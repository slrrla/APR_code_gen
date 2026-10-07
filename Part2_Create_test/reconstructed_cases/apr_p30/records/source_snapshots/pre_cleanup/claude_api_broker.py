"""Network-only Anthropic broker; repair workers never receive a credential.

Run this process with network permission. It only reads request JSON from its
queue and calls the two authorized Anthropic models; it never executes code.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

MODELS = {"claude-sonnet-5-5", "claude-haiku-4-5-20251001"}


def user_credential(session: Path) -> str:
    key = None
    for line in session.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        payload = obj.get("payload", {})
        if obj.get("type") == "response_item" and payload.get("role") == "user":
            matches = re.findall(r"sk-ant-[A-Za-z0-9_-]+", json.dumps(payload.get("content", [])))
            if matches:
                key = matches[-1]
    if not key:
        raise ValueError("No user-supplied credential found in the specified conversation")
    return key


def atomic_json(path: Path, value) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    os.replace(temp, path)


def api_request(payload: dict, key: str) -> dict:
    if not isinstance(payload, dict):
        return {"error": {"type": "invalid_request", "message": "Request must be a JSON object"}}
    if payload.get("model") not in MODELS:
        return {"error": {"type": "unauthorized_model", "message": "Model is outside this experiment"}}
    if set(payload) - {"model", "system", "messages", "max_tokens", "tools", "tool_choice", "thinking", "output_config"}:
        return {"error": {"type": "invalid_request", "message": "Unexpected Messages request fields"}}
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    deadline = time.monotonic() + 180
    for attempt in range(3):
        try:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return {"error": {"type": "TimeoutError", "message": "API request deadline exceeded"}}
            with urllib.request.urlopen(request, timeout=min(120, remaining)) as response:
                result = json.load(response)
            if result.get("model") != payload["model"]:
                return {"error": {"type": "model_mismatch", "message": "Unexpected response model"}}
            return result
        except urllib.error.HTTPError as error:
            raw = error.read().decode("utf-8", "replace").replace(key, "[REDACTED]")
            try:
                detail = json.loads(raw).get("error", {})
            except ValueError:
                detail = {"type": "http_error", "message": "Non-JSON API error"}
            if error.code in {429, 529} and attempt < 2:
                retry = error.headers.get("retry-after", "5")
                delay = min(30, max(1, float(retry))) if re.fullmatch(r"\d+(?:\.\d+)?", retry) else 5
                if time.monotonic() + delay >= deadline:
                    return {"error": detail, "http_status": error.code}
                time.sleep(delay)
                continue
            return {"error": detail, "http_status": error.code}
        except Exception as error:
            # Do not retry ambiguous network failures: a response could have been billed.
            return {"error": {"type": type(error).__name__, "message": str(error).replace(key, "[REDACTED]")}}
    raise AssertionError("Unreachable")


def serve(queue: Path, key: str) -> None:
    queue.mkdir(parents=True, exist_ok=True)
    seen = set()
    pending = {}
    atomic_json(queue / "ready.json", {"ready": True, "allowed_models": sorted(MODELS),
                                      "broker_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    with ThreadPoolExecutor(max_workers=4) as pool:
        while True:
            for source in sorted(queue.glob("*.request.json")):
                request_id = source.name.removesuffix(".request.json")
                if request_id in seen or not re.fullmatch(r"[0-9a-f]{32}", request_id):
                    continue
                seen.add(request_id)
                response_path = queue / (request_id + ".response.json")
                if response_path.exists():
                    continue  # A restart must never rebill completed requests.
                claimed = queue / (request_id + ".claimed.json")
                if claimed.exists():
                    atomic_json(response_path, {"error": {"type": "ambiguous_previous_request",
                                                         "message": "Previous broker stopped during this request; automatic replay disabled"}})
                    continue
                try:
                    payload = json.loads(source.read_text(encoding="utf-8"))
                    atomic_json(claimed, {"claimed": True, "model": payload.get("model") if isinstance(payload, dict) else None})
                    pending[pool.submit(api_request, payload, key)] = request_id
                except (ValueError, OSError):
                    atomic_json(queue / (request_id + ".response.json"),
                                {"error": {"type": "invalid_request", "message": "Malformed request JSON"}})
            for future in list(pending):
                if future.done():
                    request_id = pending.pop(future)
                    try:
                        response = future.result()
                    except Exception as error:
                        response = {"error": {"type": type(error).__name__, "message": str(error).replace(key, "[REDACTED]")}}
                    atomic_json(queue / (request_id + ".response.json"), response)
            if (queue / "stop").exists() and not pending:
                break
            time.sleep(0.1)
    atomic_json(queue / "stopped.json", {"stopped": True, "requests": len(seen)})
    print("Anthropic broker stopped; requests:", len(seen), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--credential-session", type=Path, required=True)
    args = parser.parse_args()
    serve(args.queue.resolve(), user_credential(args.credential_session))
