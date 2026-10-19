"""Network-only OpenAI Responses broker for the three authorized GPT APR runs.

Repair workers exchange JSON with this process and never receive its key. No
command or model-provided tool is executed here. Completed or claimed requests
are never replayed, including after a broker restart.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timezone
import getpass
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
MODELS = frozenset({"gpt-6-astra", "gpt-6-luna", "gpt-6-sol"})
RESPONSES_URL = "https://api.openai.com/v1/responses"
MODELS_URL = "https://api.openai.com/v1/models"
PREFLIGHT_PATH = ROOT / "records" / "gpt_p30_api_preflight.json"
BASH_TOOL = {
    "type": "function", "name": "bash", "strict": True,
    "description": "Execute one bash command in the repair workspace.",
    "parameters": {"type": "object", "properties": {"command": {"type": "string"}},
                   "required": ["command"], "additionalProperties": False},
}


def atomic_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _redact(value, key: str):
    if isinstance(value, str):
        return value.replace(key, "[REDACTED]") if key else value
    if isinstance(value, list):
        return [_redact(item, key) for item in value]
    if isinstance(value, dict):
        return {_redact(name, key): _redact(item, key) for name, item in value.items()}
    return value


def _error(kind: str, message: str, **extra) -> dict:
    return {"error": {"type": kind, "message": message}, **extra}


def _validate_key(key: str | None) -> str:
    value = (key or "").strip()
    if not re.fullmatch(r"sk-[A-Za-z0-9_-]+", value):
        raise ValueError("A valid OPENAI_API_KEY is required; the supplied value was not logged")
    return value


def _windows_user_key() -> str | None:
    if os.name != "nt":
        return None
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as registry:
            value, _ = winreg.QueryValueEx(registry, "OPENAI_API_KEY")
            return value if isinstance(value, str) else None
    except OSError:
        return None


def load_key(key_file: Path | None = None, prompt_key: bool = False) -> str:
    """Load only explicitly supplied credentials; never inspect Codex auth files."""
    if key_file is not None and prompt_key:
        raise ValueError("Choose either --key-file or --prompt-key")
    if key_file is not None:
        raw = key_file.read_text(encoding="utf-8-sig").strip()
        if re.fullmatch(r"sk-[A-Za-z0-9_-]+", raw):
            return _validate_key(raw)
        matches = []
        for line in raw.splitlines():
            match = re.fullmatch(r"\s*(?:export\s+)?OPENAI_API_KEY\s*=\s*(.*?)\s*", line)
            if match:
                value = match.group(1)
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                matches.append(value)
        if len(matches) != 1:
            raise ValueError("Key file must contain one OPENAI_API_KEY assignment or one plain key")
        return _validate_key(matches[0])
    if prompt_key:
        return _validate_key(getpass.getpass("OpenAI API key (hidden): "))
    return _validate_key(os.environ.get("OPENAI_API_KEY") or _windows_user_key())


def _request_json(url: str, key: str, payload: dict | None = None) -> dict:
    if url not in {RESPONSES_URL, MODELS_URL}:
        return _error("unauthorized_endpoint", "Endpoint is outside this experiment")
    request = urllib.request.Request(
        url, data=None if payload is None else json.dumps(payload, allow_nan=False).encode("utf-8"),
        method="GET" if payload is None else "POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    deadline = time.monotonic() + 180
    for attempt in range(3):
        try:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return _error("TimeoutError", "API request deadline exceeded; automatic replay disabled")
            # Disable redirects: a credential must never follow a Location header.
            opener = urllib.request.build_opener(_NoRedirect())
            with opener.open(request, timeout=min(120, remaining)) as response:
                result = json.load(response)
            if not isinstance(result, dict):
                return _error("invalid_response", "API response was not a JSON object")
            return _redact(result, key)
        except urllib.error.HTTPError as error:
            try:
                raw = _redact(json.loads(error.read().decode("utf-8", "replace")), key)
                detail = raw.get("error", {}) if isinstance(raw, dict) else {}
                if not isinstance(detail, dict):
                    detail = {}
            except (ValueError, OSError):
                detail = {}
            safe = {name: detail[name] for name in ("type", "message", "code", "param")
                    if name in detail and isinstance(detail[name], (str, int, float, bool, type(None)))}
            safe.setdefault("type", "http_error")
            safe.setdefault("message", "API rejected the request")
            # Only explicit rejection responses permit retries. Timeouts, dropped
            # connections, and all other errors may already have been billed.
            if error.code in {429, 503} and attempt < 2:
                retry = error.headers.get("Retry-After", "5") if error.headers else "5"
                delay = min(30.0, max(1.0, float(retry))) if re.fullmatch(r"\d+(?:\.\d+)?", retry) else 5.0
                if time.monotonic() + delay < deadline:
                    time.sleep(delay)
                    continue
            return {"error": safe, "http_status": error.code}
        except Exception as error:
            return _error(type(error).__name__, _redact(str(error), key))
    raise AssertionError("Unreachable")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def _valid_input(value) -> bool:
    if isinstance(value, str):
        return True
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        kind = item.get("type", "message")
        if kind == "message":
            if item.get("role") not in {"system", "developer", "user", "assistant"}:
                return False
            content = item.get("content")
            if isinstance(content, str):
                continue
            if not isinstance(content, list) or any(
                not isinstance(part, dict) or part.get("type") not in {"input_text", "output_text", "refusal"}
                or not isinstance(part.get("refusal") if part.get("type") == "refusal" else part.get("text"), str)
                for part in content
            ):
                return False
        elif kind == "function_call":
            if item.get("name") != "bash" or not all(isinstance(item.get(name), str) for name in ("call_id", "arguments")):
                return False
        elif kind == "function_call_output":
            if not isinstance(item.get("call_id"), str) or not isinstance(item.get("output"), str):
                return False
        elif kind == "reasoning":
            if "encrypted_content" in item and not isinstance(item["encrypted_content"], str):
                return False
        else:
            return False
    return True


def validate_payload(payload) -> dict | None:
    if not isinstance(payload, dict):
        return _error("invalid_request", "Request must be a JSON object")
    if payload.get("model") not in MODELS:
        return _error("unauthorized_model", "Model is outside this experiment")
    allowed = {"model", "input", "tools", "tool_choice", "parallel_tool_calls", "max_output_tokens", "store", "include", "reasoning"}
    if set(payload) - allowed or not _valid_input(payload.get("input")):
        return _error("invalid_request", "Unexpected Responses fields or input types")
    if payload.get("tools") != [BASH_TOOL] or payload.get("tool_choice") != "auto":
        return _error("invalid_request", "Only the experiment's bash function with automatic selection is permitted")
    if payload.get("parallel_tool_calls") is not False or payload.get("store") is not False:
        return _error("invalid_request", "Parallel tools and server-side storage must be disabled")
    if type(payload.get("max_output_tokens")) is not int or payload["max_output_tokens"] != 8192:
        return _error("invalid_request", "This experiment requires max_output_tokens=8192")
    if payload.get("include") != ["reasoning.encrypted_content"]:
        return _error("invalid_request", "Only encrypted reasoning replay may be requested")
    if "reasoning" in payload:
        reasoning = payload["reasoning"]
        if not isinstance(reasoning, dict) or set(reasoning) != {"effort"} or reasoning.get("effort") not in {
            "none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"
        }:
            return _error("invalid_request", "Unexpected explicit reasoning setting")
    return None


def _matching_model(requested: str, observed: str) -> bool:
    return observed == requested or re.fullmatch(re.escape(requested) + r"-\d{4}-\d{2}-\d{2}", observed) is not None


def api_request(payload: dict, key: str, accepted_response_models: dict[str, list[str]] | None = None) -> dict:
    problem = validate_payload(payload)
    if problem is not None:
        return problem
    result = _request_json(RESPONSES_URL, key, payload)
    if result.get("object") != "response":
        return result
    requested = payload["model"]
    accepted = {requested}
    for candidate in (accepted_response_models or {}).get(requested, []):
        if isinstance(candidate, str) and _matching_model(requested, candidate):
            accepted.add(candidate)
    if result.get("model") not in accepted:
        return _error("model_mismatch", "Unexpected response model; automatic replay disabled", native_response=result)
    return result


def preflight(key: str) -> dict:
    """Read model availability, without making generation calls or storing auth."""
    result = _request_json(MODELS_URL, key)
    base = {"checked_at": datetime.now(timezone.utc).isoformat(), "endpoint": MODELS_URL,
            "requested_models": sorted(MODELS), "ok": False}
    if "error" in result:
        return {**base, **result}
    data = result.get("data")
    if not isinstance(data, list):
        return {**base, **_error("invalid_response", "Models response has no model list")}
    models = []
    for item in data:
        if isinstance(item, dict) and isinstance(item.get("id"), str) and any(_matching_model(model, item["id"]) for model in MODELS):
            models.append({name: item[name] for name in ("id", "object", "created", "owned_by") if name in item})
    ids = {item["id"] for item in models}
    availability = {model: model in ids for model in sorted(MODELS)}
    return {**base, "ok": all(availability.values()), "availability": availability,
            "models": models, "accepted_response_models": {
                model: sorted(candidate for candidate in ids if _matching_model(model, candidate))
                for model in sorted(MODELS)}}


@contextmanager
def _broker_lock(queue: Path):
    """OS lock is released on a crash; durable claims still prevent replay."""
    with (queue / ".broker.lock").open("a+b") as stream:
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _claim(path: Path, model: str) -> bool:
    try:
        with path.open("x", encoding="utf-8") as stream:
            json.dump({"claimed": True, "model": model, "claimed_at": datetime.now(timezone.utc).isoformat()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        return True
    except FileExistsError:
        return False


def serve(queue: Path, key: str) -> dict:
    queue = queue.resolve()
    queue.mkdir(parents=True, exist_ok=True)
    with _broker_lock(queue):
        # Remove a stale ready receipt before checking current access.
        (queue / "ready.json").unlink(missing_ok=True)
        checked = preflight(key)
        atomic_json(PREFLIGHT_PATH, checked)
        if not checked["ok"]:
            atomic_json(queue / "preflight_failed.json", checked)
            return checked
        seen = set()
        pending = {}
        accepted = checked["accepted_response_models"]
        startup = {
            "ready": True, "preflight_ok": True, "allowed_models": sorted(MODELS),
            "accepted_response_models": accepted, "preflight_checked_at": checked["checked_at"],
            "broker_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        }
        atomic_json(queue / "startup.json", startup)
        atomic_json(queue / "ready.json", startup)
        with ThreadPoolExecutor(max_workers=3) as pool:
            while True:
                if not (queue / "stop").exists():
                    for source in sorted(queue.glob("*.request.json")):
                        request_id = source.name.removesuffix(".request.json")
                        if request_id in seen or not re.fullmatch(r"[0-9a-f]{32}", request_id):
                            continue
                        seen.add(request_id)
                        response_path = queue / (request_id + ".response.json")
                        if response_path.exists():
                            continue
                        try:
                            payload = json.loads(source.read_text(encoding="utf-8"))
                            problem = validate_payload(payload)
                            if problem is not None:
                                atomic_json(response_path, problem)
                                continue
                            if not _claim(queue / (request_id + ".claimed.json"), payload["model"]):
                                atomic_json(response_path, _error("ambiguous_previous_request", "Previous broker claimed this request; automatic replay disabled"))
                                continue
                            pending[pool.submit(api_request, payload, key, accepted)] = request_id
                        except (ValueError, OSError):
                            atomic_json(response_path, _error("invalid_request", "Unable to read or durably claim request JSON"))
                for future in list(pending):
                    if future.done():
                        request_id = pending.pop(future)
                        try:
                            response = future.result()
                        except Exception as error:
                            response = _error(type(error).__name__, _redact(str(error), key))
                        atomic_json(queue / (request_id + ".response.json"), _redact(response, key))
                if (queue / "stop").exists() and not pending:
                    break
                time.sleep(0.1)
        stopped = {"stopped": True, "requests_seen": len(seen)}
        atomic_json(queue / "stopped.json", stopped)
        (queue / "ready.json").unlink(missing_ok=True)
        return stopped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=ROOT / "records" / "gpt_p30_api_queue")
    credential = parser.add_mutually_exclusive_group()
    credential.add_argument("--key-file", type=Path)
    credential.add_argument("--prompt-key", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    try:
        key = load_key(args.key_file, args.prompt_key)
        if args.preflight_only:
            result = preflight(key)
            atomic_json(PREFLIGHT_PATH, result)
            print("OpenAI model preflight:", "passed" if result["ok"] else "failed", flush=True)
            return 0 if result["ok"] else 2
        result = serve(args.queue, key)
        print("OpenAI broker:", "stopped" if result.get("stopped") else "preflight failed", flush=True)
        return 0 if result.get("stopped") else 2
    except (ValueError, OSError):
        print("OpenAI broker could not load credentials or access its queue; no credential value was logged", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
