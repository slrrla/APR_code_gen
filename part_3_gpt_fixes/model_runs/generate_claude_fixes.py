"""Generate Claude fixes from the frozen GPT prompt and 73 case inputs."""

import argparse
import json
import os
from collections import Counter
from pathlib import Path

from generate_fixes import (
    atomic_text,
    export_report,
    load_experiment,
    read_json,
    redact_error,
    sha,
    utcnow,
    write_json,
)


MODELS = (
    "claude-opus-5-5",
    "claude-sonnet-5-5",
    "claude-haiku-5-5",
)
MAX_TOKENS = 16384


def request_for(root, model, entry):
    frozen = read_json(root / "_shared" / "inputs" / entry["case"] / "messages.json")
    if [message["role"] for message in frozen] != ["system", "user"]:
        raise ValueError(f"Unexpected frozen message roles for {entry['case']}")
    return {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "system": frozen[0]["content"],
        "messages": [frozen[1]],
        "output_config": {"effort": "medium"},
    }


def check_saved(root, model, manifest):
    problems = []
    for entry in manifest["cases"]:
        folder = root / model / "generation" / entry["case"]
        status_path = folder / "status.json"
        if not status_path.is_file():
            continue
        state = read_json(status_path)
        if state.get("model") != model or state.get("input_sha256") != entry["input_sha256"]["messages.json"]:
            problems.append(f"{entry['case']}: model/input mismatch")
        if state.get("fix_created"):
            fix = folder / state.get("fix_file", "")
            if not fix.is_file() or sha(fix.read_bytes()) != state.get("fix_sha256"):
                problems.append(f"{entry['case']}: saved fix missing or changed")
        request_path = folder / "request.json"
        if request_path.is_file() and read_json(request_path) != request_for(root, model, entry):
            problems.append(f"{entry['case']}: saved request differs")
    if problems:
        raise RuntimeError("\n".join(problems))


def finish_response(folder, entry, model, response, helper):
    raw = "\n".join(
        block.get("text", "")
        for block in response.get("content", [])
        if block.get("type") == "text"
    )
    atomic_text(folder / "raw_reply.txt", raw)
    state = {
        "case": entry["case"],
        "model": model,
        "reasoning_effort": "medium",
        "completed_utc": utcnow(),
        "returned_model": response.get("model"),
        "response_id": response.get("id"),
        "stop_reason": response.get("stop_reason"),
        "usage": response.get("usage"),
        "fix_created": False,
        "syntax_check": "NOT CHECKED",
        "error": "",
        "status": "RESPONSE_ERROR",
        "fix_file": None,
        "input_sha256": entry["input_sha256"]["messages.json"],
    }
    if raw.strip():
        code = helper.extract_code(raw)
        path = folder / ("fix_" + entry["case"].removeprefix("issue_") + ".py")
        atomic_text(path, code)
        state.update(fix_created=True, fix_file=path.name, fix_sha256=sha(path.read_bytes()))
        try:
            compile(code, str(path), "exec")
            state.update(syntax_check="OK", status="CREATED")
        except (SyntaxError, ValueError) as exc:
            state.update(syntax_check="ERROR", status="SYNTAX_ERROR", error=f"{type(exc).__name__}: {exc}")
    else:
        state["error"] = "No text response; no code file created."
    if response.get("stop_reason") != "end_turn":
        state["status"] = "INCOMPLETE_RESPONSE"
        state["error"] = f"stop_reason={response.get('stop_reason')}; review saved response. " + state["error"]
    write_json(folder / "status.json", state)
    return state


def run_generation(root, model, manifest, helper, client, key, limit, retry_api_errors):
    check_saved(root, model, manifest)
    export_report(root, model, manifest)
    attempted = 0
    for entry in manifest["cases"]:
        folder = root / model / "generation" / entry["case"]
        status_path = folder / "status.json"
        state = read_json(status_path) if status_path.is_file() else {}
        if state and (state.get("status") != "API_ERROR" or not retry_api_errors):
            print(f"SKIP {entry['case']}: {state['status']}", flush=True)
            continue
        if (folder / "response.json").is_file():
            finish_response(folder, entry, model, read_json(folder / "response.json"), helper)
            export_report(root, model, manifest)
            continue
        if (folder / "inflight.json").exists() and not retry_api_errors:
            print(f"PAUSED {entry['case']}: inspect interrupted request before retrying.", flush=True)
            break
        if limit is not None and attempted >= limit:
            break
        folder.mkdir(parents=True, exist_ok=True)
        request = request_for(root, model, entry)
        write_json(folder / "request.json", request)
        write_json(folder / "inflight.json", {"started_utc": utcnow(), "model": model, "case": entry["case"]})
        attempted += 1
        print(f"Processing {model} / {entry['case']} ...", flush=True)
        try:
            response = client.messages.create(**request)
        except Exception as exc:
            error = redact_error(exc, key)
            state = {
                "case": entry["case"], "model": model, "reasoning_effort": "medium",
                "status": "API_ERROR", "fix_created": False, "error": error,
                "input_sha256": entry["input_sha256"]["messages.json"],
                "completed_utc": utcnow(),
            }
            write_json(status_path, state)
            with (folder / "api_errors.jsonl").open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(state) + "\n")
            (folder / "inflight.json").unlink(missing_ok=True)
            export_report(root, model, manifest)
            print(f"ERROR {entry['case']}: {error}", flush=True)
            if getattr(exc, "status_code", None) in (400, 401, 403, 404, 429):
                print("Stopping this model: check access, settings, or quota before retrying.", flush=True)
                break
            continue
        write_json(folder / "response.json", response.model_dump(mode="json"))
        state = finish_response(folder, entry, model, read_json(folder / "response.json"), helper)
        (folder / "inflight.json").unlink(missing_ok=True)
        export_report(root, model, manifest)
        print(f"{entry['case']}: {state['status']}", flush=True)
    check_saved(root, model, manifest)
    counts = export_report(root, model, manifest)
    print(f"{model}: {dict(counts)}", flush=True)
    print(f"Report: {root / model / 'reports' / 'generation_report.csv'}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODELS, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true", help="Offline prompt/input checks; no API call")
    mode.add_argument("--check-access", action="store_true", help="Read model metadata; no generation")
    mode.add_argument("--status", action="store_true", help="Verify saved artifacts and refresh report")
    parser.add_argument("--limit", type=int, help="Maximum new API requests")
    parser.add_argument("--retry-api-errors", action="store_true", help="Explicitly retry failed/interrupted requests")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")

    root = Path(__file__).resolve().parent
    manifest, helper = load_experiment(root)
    check_saved(root, args.model, manifest)
    if args.preflight:
        for entry in manifest["cases"]:
            request_for(root, args.model, entry)
        print(f"OFFLINE OK: {args.model}, medium; 73 identical prompt inputs; 1015 assigned case/version pairs.")
        print("No credentials read, no API requests made, no generated code executed.")
        return
    if args.status:
        print(dict(export_report(root, args.model, manifest)))
        return

    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in this PowerShell session.")
    from anthropic import Anthropic

    client = Anthropic(api_key=key, max_retries=0, timeout=600.0)
    if args.check_access:
        try:
            info = client.models.retrieve(args.model)
            print(f"Model metadata accessible: {info.id}. Generation access is confirmed by the first real request.")
        except Exception as exc:
            raise RuntimeError(redact_error(exc, key)) from None
        return

    lock = root / args.model / "generation.lock"
    try:
        with lock.open("x", encoding="utf-8") as handle:
            json.dump({"pid": os.getpid(), "started_utc": utcnow()}, handle)
    except FileExistsError:
        raise RuntimeError(f"Generation lock exists: {lock}. Check for a live run before removing it.") from None
    try:
        run_generation(root, args.model, manifest, helper, client, key, args.limit, args.retry_api_errors)
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
