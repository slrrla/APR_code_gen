"""Read-only provenance and native Responses usage audit for all 90 GPT APR runs.

No API calls, credential loading, benchmark execution or reference/test parsing.
Original programs and validators are opened only as bytes for hashes. --write
can write only new GPT audit reports; no run evidence is repaired or rewritten.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re

# Reuse the original read-only command classifications, including its documented
# false positives. No experimental harness or model is imported or executed.
from audit_claude_runs import (Auditor as CommandAuditor, DEFAULT_AGENT_SOURCE,
                               EMPTY_SHA256, IncompleteRunError, LIMITATIONS,
                               SOURCES, read_json, redact)

ROOT = Path(__file__).resolve().parent.parent
MODELS = {"gpt6astrap30": "gpt-6-astra", "gpt6lunap30": "gpt-6-luna", "gpt6solp30": "gpt-6-sol"}
HARNESSES = {"gpt_p30.py", "openai_model.py", "openai_api_broker.py", "adapter.py", "claude_environment.py", "claude_model.py"}
PRICES = {model: dict(zip(("input_per_million", "output_per_million", "cache_read_per_million", "cache_write_per_million"), rates))
          for model, rates in (("gpt-6-astra", (10, 50, 1, 12.5)), ("gpt-6-luna", (.1, .5, .01, .125)), ("gpt-6-sol", (2, 10, .2, 2.5)))}
LONG_CONTEXT = {"long_context_threshold_input_tokens": 272000, "long_context_input_multiplier": 2.0, "long_context_output_multiplier": 1.5}
QUESTION_APPENDIX = (
    "\n\n## Original user question (solution sections removed)\n{{question}}\n"
    "\nOnly inspect and edit this task workspace and installed dependency APIs. "
    "Reference fixes, evaluation tests, other cases and previous repairs are unavailable inputs.\n"
)
BASH_TOOL = {
    "type": "function", "name": "bash", "description": "Execute one bash command in the repair workspace.",
    "strict": True, "parameters": {"type": "object", "properties": {"command": {"type": "string"}},
                                  "required": ["command"], "additionalProperties": False},
}


def default_queue_path(root: Path) -> Path:
    return Path(root) / "records/gpt_p30_api_queue"


def finite_number(value) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)


def close_cost(left, right, tolerance=1e-8) -> bool:
    return finite_number(left) and finite_number(right) and math.isclose(left, right, abs_tol=tolerance, rel_tol=0)


def usage_cost(prices: dict, usage: dict) -> float:
    """Independent accounting: cached input and reasoning are already included.

    Cache writes are never inferred. A nonstandard explicit write count requires
    its own declared rate. Invalid/missing usage is unknown, never assumed free.
    """
    if not isinstance(prices, dict) or not isinstance(usage, dict):
        raise ValueError("Prices and native usage must be objects")
    if not {"input_tokens", "output_tokens"} <= set(usage):
        raise ValueError("Native input/output usage is missing")

    def count(values, name):
        value = values.get(name, 0)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Invalid native token count: " + name)
        return value

    def rate(name, required=True):
        value = prices.get(name)
        if value is None and not required:
            return 0
        if not finite_number(value) or value < 0:
            raise ValueError("Missing/invalid explicit price: " + name)
        return value

    input_tokens, output_tokens = count(usage, "input_tokens"), count(usage, "output_tokens")
    input_detail = usage.get("input_tokens_details", {})
    output_detail = usage.get("output_tokens_details", {})
    if not isinstance(input_detail, dict) or not isinstance(output_detail, dict):
        raise ValueError("Native token details must be objects")
    cached, written = count(input_detail, "cached_tokens"), count(input_detail, "cache_write_tokens")
    if cached + written > input_tokens or count(output_detail, "reasoning_tokens") > output_tokens:
        raise ValueError("Native token detail exceeds total")
    if "total_tokens" in usage and count(usage, "total_tokens") != input_tokens + output_tokens:
        raise ValueError("Native total tokens disagree")
    for key, expected in LONG_CONTEXT.items():
        if prices.get(key, expected) != expected:
            raise ValueError("Unsupported long-context pricing setting")
    large = input_tokens > LONG_CONTEXT["long_context_threshold_input_tokens"]
    input_multiplier, output_multiplier = (2, 1.5) if large else (1, 1)
    input_cost = ((input_tokens - cached - written) * rate("input_per_million")
                  + cached * rate("cache_read_per_million", bool(cached))
                  + written * rate("cache_write_per_million", bool(written)))
    return (input_cost * input_multiplier + output_tokens * rate("output_per_million") * output_multiplier) / 1_000_000


def accepted_models(model, manifest):
    accepted = manifest.get("accepted_response_models", [model])
    if not isinstance(accepted, list) or not accepted or len(set(accepted)) != len(accepted):
        raise ValueError("Invalid accepted response model list")
    for name in accepted:
        if not isinstance(name, str) or not (name == model or re.fullmatch(re.escape(model) + r"-\d{4}-\d{2}-\d{2}", name)):
            raise ValueError("Only exact requested model or explicitly accepted dated snapshot is permitted")
    return set(accepted) | {model}


def history_input(messages):
    """Reconstruct request input without loading the model implementation."""
    history = []
    for message in messages:
        role, content = message.get("role"), message.get("content", "")
        if role in {"assistant", "user"} and isinstance(content, list):
            if role == "user" and not all(isinstance(item, dict) and item.get("type") == "function_call_output" for item in content):
                raise ValueError("Unexpected native user input list")
            history.extend(content)
        elif role in {"system", "user", "assistant"} and isinstance(content, str):
            history.append({"role": role, "content": content})
        else:
            raise ValueError("Unexpected trajectory input role/content")
    return history


def trajectory_usage(trajectory: dict, model: str, prices: dict, accepted=None) -> dict:
    entries, problems = [], []
    allowed = set(accepted or [model]) | {model}
    messages = trajectory.get("messages", [])
    for index, message in enumerate(messages):
        if message.get("role") != "assistant":
            continue
        extra = message.get("extra", {})
        response = extra.get("response")
        try:
            if not isinstance(response, dict) or response.get("object") != "response":
                raise ValueError("Assistant message missing native Responses object")
            if response.get("model") not in allowed:
                raise ValueError("Native response model mismatch")
            if not isinstance(response.get("id"), str) or not response["id"]:
                raise ValueError("Native response ID is missing")
            if not isinstance(response.get("output"), list) or message.get("content") != response["output"] or extra.get("usage") != response.get("usage"):
                raise ValueError("Native output/usage was not retained unchanged")
            cost = usage_cost(prices, response["usage"])
            if extra.get("cost_status") != "priced" or not close_cost(cost, extra.get("cost"), 1e-10):
                raise ValueError("Native cost unknown or differs from usage")
            stamp = extra.get("timestamp")
            if not finite_number(stamp) or not finite_number(response.get("created_at")):
                raise ValueError("Native timestamp missing or invalid")
            if response["created_at"] > stamp + 2:
                raise ValueError("Native response predates its creation timestamp")
            actions = extra.get("actions", [])
            if not isinstance(actions, list):
                raise ValueError("Native actions must be a list")
            calls = [item for item in response["output"] if item.get("type") == "function_call"]
            if actions:
                if response.get("status") != "completed" or len(calls) != 1 or calls[0].get("name") != "bash" or calls[0].get("status") not in (None, "completed"):
                    raise ValueError("Incomplete or invalid response executed an action")
                arguments = json.loads(calls[0]["arguments"])
                if set(arguments) != {"command"} or actions != [{"command": arguments["command"], "tool_call_id": calls[0].get("call_id")}]:
                    raise ValueError("Executable actions differ from native function arguments")
            if response.get("status") not in {"completed", "incomplete"}:
                raise ValueError("Native terminal status is not completed/incomplete")
            entries.append({"id": response["id"], "cost_usd": cost, "usage": response["usage"],
                            "has_executable_action": bool(actions), "timestamp": stamp,
                            "created_at": response["created_at"], "message_index": index, "response": response})
        except (KeyError, TypeError, ValueError) as error:
            problems.append(redact(str(error)))
    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)):
        problems.append("Duplicate native response IDs in trajectory")
    return {"native_responses": len(entries), "cost_usd": sum(entry["cost_usd"] for entry in entries),
            "billed_turns_without_executable_action": sum(not entry["has_executable_action"] for entry in entries),
            "response_ids": ids, "last_response_timestamp": max((entry["timestamp"] for entry in entries), default=0),
            "entries": entries, "problems": problems}


class Auditor(CommandAuditor):
    def __init__(self, root: Path, queue: Path | None = None, default_agent_source: Path = DEFAULT_AGENT_SOURCE):
        super().__init__(Path(root), Path(queue or default_queue_path(root)), Path(default_agent_source))
        self.prices, self.manifests, self.claimed_requests = {}, {}, set()

    def confined(self, path, base=None):
        base = Path(base or self.root).resolve()
        path = Path(path)
        result = (base / path).resolve() if not path.is_absolute() else path.resolve()
        result.relative_to(base)
        if any(part.lower() in {".codex", ".aws", ".ssh", ".env"} for part in result.parts):
            raise ValueError("Protected configuration is never audit input")
        return result

    def preflight(self):
        missing = []
        for folder in MODELS:
            run = self.root / "runs" / folder
            for name in ("manifest.json", "experiment.json", "experiment_result.json"):
                if not (run / name).is_file():
                    missing.append(folder + "/" + name)
            if missing:
                continue
            manifest = read_json(run / "manifest.json")
            if read_json(run / "experiment.json").get("status") != "complete":
                missing.append(folder + ": experiment not complete")
            tasks = manifest.get("tasks", [])
            if len(tasks) != 30 or len({task.get("case") for task in tasks}) != 30:
                missing.append(folder + ": requires exactly 30 unique cases")
            for task in tasks:
                case = task.get("case", "")
                if not re.fullmatch(r"issue_\d+(?:_[A-Za-z0-9]+)?", case):
                    raise ValueError("Invalid selected case identifier")
                for name in ("agent_input.json", "agent_result.json", "result.json", "traj.json"):
                    if not (run / "tasks" / case / name).is_file():
                        missing.append(folder + "/" + case + "/" + name)
            self.manifests[folder] = manifest
        if missing:
            raise IncompleteRunError(f"Final audit requires all 90 completed runs ({len(missing)} incomplete; first: {missing[0]})")
        return self.manifests

    def source_freeze(self, folder, manifest):
        snapshot = self.confined(manifest["source_snapshot_directory"])
        self.check(snapshot == self.root / "records/gpt_p30_sources", "unexpected_source_snapshot_directory", folder=folder)
        sources = manifest.get("runner_sources", {})
        self.check(HARNESSES <= set(sources), "frozen_runner_sources_missing", folder=folder)
        for name, digest in sources.items():
            if Path(name).name != name or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
                raise ValueError("Invalid frozen source filename")
            frozen = self.confined(snapshot / name)
            self.check(self.digest(frozen) == digest, "frozen_source_hash_changed", folder=folder, filename=name)
            if name.endswith(".py") and (self.root / "tools" / name).is_file():
                self.check(self.digest(self.root / "tools" / name) == digest, "live_runner_source_hash_changed", folder=folder, filename=name)
        self.check(manifest.get("default_agent_source_sha256") == self.digest(self.default_agent_source), "default_agent_source_hash_changed", folder=folder)
        self.check(self.digest(snapshot / "default.py") == manifest.get("default_agent_source_sha256"), "frozen_default_agent_hash_changed", folder=folder)
        self.check(self.digest(snapshot / "apr.yaml") == self.digest(self.root / "upstream/configs/apr.yaml"), "frozen_apr_config_hash_changed", folder=folder)
        self.check(manifest.get("mini_swe_version") == "2.4.6", "manifest_mini_swe_version_changed", folder=folder)
        baseline = read_json(self.root / "runs/sonnet5.5p30/manifest.json")
        self.check(manifest.get("default_agent_source_sha256") == baseline.get("default_agent_source_sha256"), "default_agent_differs_from_claude", folder=folder)
        self.check(sources.get("claude_environment.py") == baseline.get("runner_sources", {}).get("claude_environment.py"), "monitored_environment_differs_from_claude", folder=folder)

    def load_queue(self):
        queue = self.confined(self.queue)
        receipt = queue / "startup.json"
        if not receipt.exists():
            receipt = queue / "ready.json"
        ready = read_json(receipt)
        self.check(ready.get("preflight_ok") is True and set(ready.get("allowed_models", [])) == set(MODELS.values()), "broker_preflight_missing_or_models_changed")
        for folder, manifest in self.manifests.items():
            self.check(ready.get("broker_source_sha256") == manifest["runner_sources"].get("openai_api_broker.py"), "broker_startup_source_hash_mismatch", folder=folder)
            self.check(set(ready.get("accepted_response_models", {}).get(MODELS[folder], [])) | {MODELS[folder]} == accepted_models(MODELS[folder], manifest), "broker_accepted_model_set_mismatch", folder=folder)
        requests = {path.name.removesuffix(".request.json") for path in queue.glob("*.request.json")}
        for suffix in ("response", "claimed"):
            found = {path.name.removesuffix(f".{suffix}.json") for path in queue.glob(f"*.{suffix}.json")}
            self.check(found <= requests, "orphan_broker_" + suffix + "_artifacts", request_ids=sorted(found - requests))
        for request_id in sorted(requests):
            if not re.fullmatch(r"[0-9a-f]{32}", request_id):
                raise ValueError("Invalid broker request artifact name")
            path = queue / (request_id + ".request.json")
            request = read_json(path)
            self.scan(path)
            record = {"request_id": request_id, "request": request, "request_mtime": path.stat().st_mtime}
            self.check(request.get("model") in MODELS.values(), "unauthorized_requested_model", request_id=request_id)
            claimed_path = queue / (request_id + ".claimed.json")
            self.check(claimed_path.is_file(), "broker_claim_missing", request_id=request_id)
            if claimed_path.is_file():
                claimed = read_json(claimed_path)
                self.check(claimed.get("claimed") is True and claimed.get("model") == request.get("model"), "broker_claim_identity_mismatch", request_id=request_id)
                claim_time = datetime.fromisoformat(claimed["claimed_at"])
                self.check(claim_time.tzinfo is not None and path.stat().st_mtime <= claim_time.timestamp() + 2, "broker_claim_time_invalid", request_id=request_id)
            response_path = queue / (request_id + ".response.json")
            self.check(response_path.is_file(), "broker_response_missing", request_id=request_id)
            if response_path.is_file():
                response = read_json(response_path)
                self.scan(response_path)
                record.update(response=response, response_mtime=response_path.stat().st_mtime)
                native = response.get("native_response", response)
                if native.get("object") == "response":
                    record["response"] = native
                    native_id = native.get("id")
                    self.check(isinstance(native_id, str) and bool(native_id) and native_id not in self.response_map, "duplicate_or_missing_queue_native_response_id", request_id=request_id)
                    self.response_map[native_id] = record
                else:
                    self.warning("broker_error_response", request_id=request_id, model=request.get("model"), http_status=response.get("http_status"),
                                 error_type=(response.get("error") or {}).get("type"), usage_status="not_returned; only recorded native usage is included in cost totals")
                    self.check(isinstance(response.get("error"), dict), "broker_non_native_response_without_error", request_id=request_id)
                    status = response.get("http_status")
                    self.check(isinstance(status, int) and not isinstance(status, bool) and 400 <= status < 500,
                               "broker_transport_error_has_uncertain_billed_usage", request_id=request_id, http_status=status)
            self.queue_records[request_id] = record

    def request_matches(self, request, model, history):
        return request == {"model": model, "input": history, "tools": [BASH_TOOL], "tool_choice": "auto",
                           "parallel_tool_calls": False, "max_output_tokens": 8192, "store": False,
                           "include": ["reasoning.encrypted_content"]}

    def harness_preflights(self):
        versions = {task["version"] for manifest in self.manifests.values() for task in manifest["tasks"]}
        receipts = []
        for path in sorted((self.root / "records/gpt_p30_harness_preflight").glob("*/receipt.json")):
            receipt = read_json(path)
            checks = receipt.get("checks", [])
            passed = len(checks) == len(versions) and {check.get("version") for check in checks} == versions and all(check.get("passed") is True and check.get("returncode") == 0 for check in checks)
            if not passed:
                continue
            stamp = datetime.fromisoformat(receipt["checked_at"])
            self.check(stamp.tzinfo is not None, "harness_preflight_timestamp_missing_timezone")
            for check in checks:
                directory = self.confined(path.parent / check["version"] / "command_audit")
                events = [json.loads(line) for line in (directory / "commands.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
                results = [event for event in events if event.get("event") == "result"]
                valid = len(results) == 1 and results[0].get("command") == '$PY -c "print(731942)"' and results[0].get("status") == "EXECUTED" and results[0].get("returncode") == 0
                if valid:
                    valid = self.confined(results[0]["stdout_log"], directory).read_bytes().strip() == b"731942"
                self.check(valid, "harness_preflight_evidence_mismatch", receipt=path.parent.name, version=check["version"])
            receipts.append({"receipt": path.parent.name, "checked_at": receipt["checked_at"], "timestamp": stamp.timestamp(), "versions": sorted(versions)})
        self.check(bool(receipts), "passing_prepaid_harness_preflight_missing")
        if receipts and self.queue_records:
            first = min(record["request_mtime"] for record in self.queue_records.values())
            self.check(min(receipt["timestamp"] for receipt in receipts) <= first + 2, "paid_request_preceded_harness_preflight")
        return receipts

    def reconcile_trajectory(self, folder, case, trajectory, agent, manifest):
        model = MODELS[folder]
        tally = trajectory_usage(trajectory, model, self.prices[model], accepted_models(model, manifest))
        for problem in tally["problems"]:
            self.check(False, "native_trajectory_integrity", folder=folder, case=case, problem=problem)
        stats, messages = trajectory.get("info", {}).get("model_stats", {}), trajectory.get("messages", [])
        self.check(close_cost(tally["cost_usd"], agent.get("cost_usd")) and close_cost(tally["cost_usd"], stats.get("instance_cost")), "trajectory_cost_mismatch", folder=folder, case=case)
        self.check(stats.get("api_calls") == agent.get("steps") and isinstance(agent.get("steps"), int) and not isinstance(agent.get("steps"), bool), "trajectory_call_count_mismatch", folder=folder, case=case)
        request_times, response_times = [], []
        matched_requests = set()
        for entry in tally["entries"]:
            native_id = entry["id"]
            record = self.response_map.get(native_id)
            self.check(record is not None, "native_response_missing_from_broker_queue", folder=folder, case=case, response_id=native_id)
            self.check(native_id not in self.used_response_ids, "native_response_reused_across_trajectories", folder=folder, case=case, response_id=native_id)
            self.used_response_ids.add(native_id)
            if record is None:
                continue
            self.check(record["response"] == entry["response"], "broker_response_differs_from_trajectory", folder=folder, case=case, response_id=native_id)
            self.check(self.request_matches(record["request"], model, history_input(messages[:entry["message_index"]])), "broker_request_history_or_settings_mismatch", folder=folder, case=case, response_id=native_id)
            matched_requests.add(record["request_id"])
            request_times.append(record["request_mtime"])
            response_times.append(record["response_mtime"])
        # A transport failure has no assistant native response, but is still a
        # counted DefaultAgent call. Match its exact final request prefix.
        prefix = messages[:-1] if messages and messages[-1].get("role") == "exit" else messages
        for request_id, record in self.queue_records.items():
            if record.get("response", {}).get("object") == "response" or request_id in matched_requests:
                continue
            if self.request_matches(record["request"], model, history_input(prefix)):
                matched_requests.add(request_id)
                request_times.append(record["request_mtime"])
                response_times.append(record.get("response_mtime", 0))
        self.check(not (matched_requests & self.claimed_requests), "broker_request_claimed_by_multiple_trajectories", folder=folder, case=case)
        self.claimed_requests.update(matched_requests)
        self.check(len(matched_requests) == agent.get("steps"), "native_and_error_requests_do_not_reconcile_steps", folder=folder, case=case)
        tally["queue_end_timestamp"] = max([0, *request_times, *response_times])
        return tally

    def prompt(self, folder, task, tdir, context, trajectory):
        from jinja2 import StrictUndefined, Template
        import yaml

        case = task["case"]
        baseline = self.root / "runs/sonnet5.5p30/tasks" / case
        self.check(context == read_json(baseline / "agent_input.json") and set(context) == {"case", "version", "title", "question"}, "initial_input_differs_from_frozen_claude", folder=folder, case=case)
        self.check(context.get("case") == case and context.get("version") == task["version"], "initial_input_identity_mismatch", folder=folder, case=case)
        self.check(not re.search(r"(?im)^\s*(?:Solution explanation|Original fixed code|Answer):", context.get("question", "")), "solution_section_in_initial_question", folder=folder, case=case)
        cfg = trajectory.get("info", {}).get("config", {})
        original = yaml.safe_load((self.root / "upstream/configs/apr.yaml").read_text(encoding="utf-8"))
        agent_cfg = original["agent"] | {"max_consecutive_format_errors": 3}
        agent_cfg["instance_template"] = agent_cfg["instance_template"].replace("/work/buggy.py", "buggy.py") + QUESTION_APPENDIX
        actual = {key: value for key, value in cfg.get("agent", {}).items() if key != "output_path"}
        claude = read_json(baseline / "traj.json")["info"]["config"]["agent"]
        self.check(actual == agent_cfg == {key: value for key, value in claude.items() if key != "output_path"}, "agent_prompt_or_budget_differs_from_frozen_claude", folder=folder, case=case)
        model_cfg = cfg.get("model", {})
        for key in ("observation_template", "format_error_template"):
            self.check(model_cfg.get(key) == original["model"][key], "model_feedback_template_changed", folder=folder, case=case, field=key)
        self.check(model_cfg.get("model_name") == MODELS[folder] and model_cfg.get("max_tokens") == 8192 and model_cfg.get("model_kwargs") == {} and model_cfg.get("reasoning_policy") == "provider_default", "model_config_mismatch", folder=folder, case=case)
        self.check(model_cfg.get("prices") == self.prices[MODELS[folder]] | LONG_CONTEXT, "model_price_configuration_mismatch", folder=folder, case=case)
        self.check(set(model_cfg.get("accepted_response_models", [])) | {MODELS[folder]} == accepted_models(MODELS[folder], self.manifests[folder]), "trajectory_model_allowlist_mismatch", folder=folder, case=case)
        commands = trajectory.get("environment_commands", [])
        self.check(bool(commands) and commands[0].get("command") == "$PY buggy.py", "initial_reproduction_command_changed", folder=folder, case=case)
        first = commands[0]
        if first.get("status") == "POLICY_REJECTED":
            error_text = "Command rejected by monitored execution policy: " + "; ".join(first.get("guard_reasons", [])) + "\n"
        else:
            output = self.confined(first["stdout_log"], tdir / "command_audit").read_bytes()
            if len(output) > 1_000_000:
                output = output[:500_000] + b"\n[output truncated; full command output retained in host audit]\n" + output[-500_000:]
            error_text = output.decode("utf-8", errors="replace")
        variables = dict(task="", title=context["title"], question=context["question"], qiskit_version=task["version"], error_text=error_text[-10000:], mcp_enabled=False)
        messages = trajectory.get("messages", [])
        expected = [{"role": role, "content": Template(agent_cfg[key], undefined=StrictUndefined).render(**variables)} for role, key in (("system", "system_template"), ("user", "instance_template"))]
        self.check([{key: message.get(key) for key in ("role", "content")} for message in messages[:2]] == expected, "rendered_initial_prompt_changed_or_extra_input", folder=folder, case=case)
        return cfg

    def audit_case(self, folder, model, task):
        case, version = task["case"], task["version"]
        tdir = self.root / "runs" / folder / "tasks" / case
        context, agent, result, trajectory = [read_json(tdir / name) for name in ("agent_input.json", "agent_result.json", "result.json", "traj.json")]
        for name in ("agent_input.json", "agent_result.json", "result.json", "traj.json"):
            self.scan(tdir / name)
        self.check(all(agent.get(key) == value for key, value in (("case", case), ("version", version), ("model", model))), "agent_identity_mismatch", folder=folder, case=case)
        source = Path(task["source_dir"]).resolve()
        if source != (self.root.parent / case).resolve():
            raise ValueError("Original source directory is outside selected case directory")
        self.check(set(task["hashes"]) == set(SOURCES), "unexpected_source_hash_fields", folder=folder, case=case)
        for name in SOURCES:
            self.check(self.digest(source / name) == task["hashes"].get(name), "original_source_hash_changed", folder=folder, case=case, filename=name)
        present = agent.get("candidate_present")
        candidate = tdir / "workspace/buggy.py"
        if present is False:
            self.check(not candidate.exists() and agent.get("candidate_sha256") == EMPTY_SHA256 and (tdir / "patched.py").stat().st_size == 0 and result.get("candidate_missing") is True and result.get("repaired") is False, "deleted_candidate_not_consistently_recorded_as_failure", folder=folder, case=case)
        else:
            self.check(present is True and self.digest(candidate) == agent.get("candidate_sha256") and result.get("candidate_missing") is False, "workspace_candidate_hash_changed", folder=folder, case=case)
        for relative, expected in (("original.py", task["hashes"]["buggy.py"]), ("validator/test.py", task["hashes"]["test.py"]), ("patched.py", agent.get("candidate_sha256"))):
            self.check(self.digest(tdir / relative) == expected, "snapshot_or_candidate_hash_changed", folder=folder, case=case, filename=relative)
        test_starts = []
        for variant, expected in (("original", task["hashes"]["buggy.py"]), ("reference", task["hashes"]["fixed.py"]), ("candidate", agent.get("candidate_sha256"))):
            record = result.get(variant, {})
            self.check(record.get("source_sha256") == expected and record.get("test_sha256") == task["hashes"]["test.py"] and record.get("interpreter") == task["interpreter"], "tested_source_or_test_or_interpreter_mismatch", folder=folder, case=case, variant=variant)
            log = read_json(tdir / "logs" / (variant + ".json"))
            self.check(log == record, "final_test_log_differs_from_result", folder=folder, case=case, variant=variant)
            duration = log["seconds"]
            if not finite_number(duration) or duration < 0:
                raise ValueError("Final test duration invalid")
            test_starts.append((tdir / "logs" / (variant + ".stdout.txt")).stat().st_mtime - duration)
        original, reference = result["original"], result["reference"]
        valid = original.get("status") in {"FAIL", "ERROR"} and original.get("tests_run", 0) > 0 and reference.get("status") == "PASS" and reference.get("tests_run", 0) > 0 and reference.get("skipped") == 0
        self.check(result.get("baseline_valid") is True and valid, "final_baseline_not_valid", folder=folder, case=case)
        patch = result.get("audit", {})
        repaired = present is True and valid and result["candidate"].get("status") == "PASS" and patch.get("changed") is True and patch.get("syntax_ok") is True and patch.get("suspicious") is False
        self.check(result.get("repaired") == repaired, "repaired_result_not_supported", folder=folder, case=case)
        info, messages = trajectory.get("info", {}), trajectory.get("messages", [])
        self.check(bool(messages) and messages[-1].get("role") == "exit" and info.get("exit_status") == agent.get("exit_status") == messages[-1].get("extra", {}).get("exit_status"), "trajectory_not_consistently_closed", folder=folder, case=case)
        cfg = self.prompt(folder, task, tdir, context, trajectory)
        self.check(cfg.get("agent_type") == "minisweagent.agents.default.DefaultAgent" and info.get("mini_version") == "2.4.6", "native_agent_type_or_version_mismatch", folder=folder, case=case)
        self.check(cfg.get("model_type") == "openai_model.OpenAIResponsesModel" and cfg.get("environment_type") == "claude_environment.MonitoredBashEnvironment", "worker_adapter_types_changed", folder=folder, case=case)
        tally = self.reconcile_trajectory(folder, case, trajectory, agent, self.manifests[folder])
        saved_extras = [message.get("extra", {}) for message in messages if message.get("extra", {}).get("response") is not None]
        self.check(agent.get("native_responses") == len(saved_extras) and agent.get("cost_statuses") == sorted({extra.get("cost_status", "unknown") for extra in saved_extras}), "agent_native_response_summary_mismatch", folder=folder, case=case)
        commands = self.commands(trajectory, tdir, folder, case)
        native_commands = [action["command"] for message in messages for action in message.get("extra", {}).get("actions", [])]
        self.check(native_commands == [command.get("command") for command in trajectory.get("environment_commands", [])[1:]], "executed_commands_differ_from_native_actions", folder=folder, case=case)
        for message in messages[2:]:
            if message.get("role") == "user":
                extra = message.get("extra", {})
                permitted = extra.get("interrupt_type") == "FormatError" or ("raw_output" in extra and "returncode" in extra and isinstance(message.get("content"), list))
                self.check(permitted, "unaccounted_user_message_after_initial_prompt", folder=folder, case=case)
        submitted = agent.get("exit_status") == "Submitted"
        self.check(agent.get("submitted") == submitted and commands["submitted_commands"] == int(submitted), "submission_records_disagree", folder=folder, case=case)
        self.check(agent.get("candidate_test_feedback") is False, "candidate_test_feedback_flag_changed", folder=folder, case=case)
        if agent.get("exit_status") == "LimitsExceeded":
            self.check(agent.get("steps", 0) >= 40 or tally["cost_usd"] >= 1, "limit_exit_without_native_budget_limit", folder=folder, case=case)
        end = max(tally["last_response_timestamp"], tally["queue_end_timestamp"], (tdir / "traj.json").stat().st_mtime, (tdir / "agent_result.json").stat().st_mtime)
        self.check(end <= min(test_starts) + 2, "final_test_started_before_agent_phase_ended", folder=folder, case=case)
        return {"case": case, "version": version, "native_responses": tally["native_responses"], "steps": agent["steps"], "cost_usd": tally["cost_usd"], "submitted": submitted, "repaired": repaired, "candidate_present": present,
                "generated_test_status": result["candidate"]["status"], "billed_turns_without_executable_action": tally["billed_turns_without_executable_action"], "agent_phase_end_timestamp": end, "estimated_first_test_start_timestamp": min(test_starts), **commands}

    def smoke(self, folder, model):
        rows = []
        for directory in ("pipeline_smoke", "pilot"):
            for path in sorted((self.root / "runs" / folder / directory).glob("*/agent_result.json")):
                agent, trajectory = read_json(path), read_json(path.with_name("traj.json"))
                tally = self.reconcile_trajectory(folder, directory + "/" + path.parent.name, trajectory, agent, self.manifests[folder])
                rows.append({"case": path.parent.name, "directory": directory, "native_responses": tally["native_responses"], "cost_usd": tally["cost_usd"]})
        return {"cases": rows, "cost_usd": sum(row["cost_usd"] for row in rows), "separate_from_official_30_case_budget": True}

    def audit_incidents(self):
        """Account frozen interrupted cohorts separately, including unissued calls.

        These are never candidate results or replacement official cases. A
        request without a broker claim was not issued by the frozen broker;
        claimed requests without native usage remain an accounting failure.
        """
        reports = []
        for directory in sorted((self.root / "records").glob("gpt_p30_environment_failure_*")):
            if not directory.is_dir():
                continue
            directory = self.confined(directory)
            label = directory.name
            receipt = read_json(directory / "incident.json")
            self.scan(directory / "incident.json")
            self.check(receipt.get("excluded_from_official_runs") is True and receipt.get("status") == "infrastructure_interrupted", "incident_exclusion_not_explicit", incident=label)
            files = read_json(directory / "archive_index.json")["files"]
            actual = {path.relative_to(directory).as_posix() for path in directory.rglob("*") if path.is_file() and path != directory / "archive_index.json"}
            self.check(set(files) == actual, "incident_archive_inventory_changed", incident=label)
            for name, metadata in files.items():
                path = self.confined(name, directory)
                self.check(path.stat().st_size == metadata["bytes"] and self.digest(path) == metadata["sha256"] and path.stat().st_mtime_ns == metadata["mtime_ns"], "incident_archive_file_changed", incident=label, filename=name)
            queue = directory / "records/gpt_p30_api_queue"
            startup = read_json(queue / "startup.json")
            native_map, requests, traced, matched = {}, {}, set(), set()
            unanswered = {entry["request_id"]: entry for entry in receipt.get("unanswered_requests", [])}
            unissued = set()
            costs = Counter()
            for path in sorted(queue.glob("*.request.json")):
                request_id = path.name.removesuffix(".request.json")
                if not re.fullmatch(r"[0-9a-f]{32}", request_id):
                    raise ValueError("Invalid incident request filename")
                request = read_json(path)
                self.scan(path)
                requests[request_id] = request
                model = request.get("model")
                self.check(model in MODELS.values(), "incident_unauthorized_model", incident=label, request_id=request_id)
                claim_path = path.with_name(request_id + ".claimed.json")
                response_path = path.with_name(request_id + ".response.json")
                if not response_path.exists():
                    unissued.add(request_id)
                    self.check(not claim_path.exists() and unanswered.get(request_id) == {"request_id": request_id, "claimed": False}, "incident_unanswered_request_not_proven_unissued", incident=label, request_id=request_id)
                    continue
                self.check(claim_path.is_file(), "incident_native_response_has_no_claim", incident=label, request_id=request_id)
                if claim_path.is_file():
                    claim = read_json(claim_path)
                    self.check(claim.get("claimed") is True and claim.get("model") == model, "incident_claim_identity_mismatch", incident=label, request_id=request_id)
                response = read_json(response_path)
                self.scan(response_path)
                response = response.get("native_response", response)
                if response.get("object") != "response":
                    self.check(False, "incident_claimed_request_without_native_usage", incident=label, request_id=request_id)
                    continue
                native_id = response.get("id")
                self.check(isinstance(native_id, str) and bool(native_id) and native_id not in native_map, "incident_duplicate_native_id", incident=label, request_id=request_id)
                native_map[native_id] = (request_id, response)
                costs[model] += usage_cost(PRICES[model], response["usage"])
            self.check(unissued == set(unanswered), "incident_unanswered_inventory_mismatch", incident=label)
            for suffix in ("claimed", "response"):
                names = {path.name.removesuffix("." + suffix + ".json") for path in queue.glob("*." + suffix + ".json")}
                self.check(names <= set(requests), "incident_orphan_broker_artifact", incident=label, kind=suffix)
            model_rows = []
            for folder, model in MODELS.items():
                run = directory / "runs" / folder
                manifest = read_json(run / "manifest.json")
                accepted = accepted_models(model, manifest)
                for name, expected in manifest["runner_sources"].items():
                    path = self.confined(Path("records/gpt_p30_sources") / name, directory)
                    self.check(self.digest(path) == expected, "incident_frozen_source_hash_changed", incident=label, folder=folder, filename=name)
                self.check(startup.get("broker_source_sha256") == manifest["runner_sources"].get("openai_api_broker.py"), "incident_broker_source_hash_mismatch", incident=label, folder=folder)
                self.check(not list((run / "tasks").glob("*/result.json")) and not list((run / "tasks").glob("*/logs/candidate.json")), "incident_has_final_test_results", incident=label, folder=folder)
                native_count = 0
                for trajectory_path in sorted((run / "tasks").glob("*/traj.json")):
                    trajectory = read_json(trajectory_path)
                    self.scan(trajectory_path)
                    tally = trajectory_usage(trajectory, model, PRICES[model], accepted)
                    native_count += tally["native_responses"]
                    self.check(not tally["problems"], "incident_native_trajectory_integrity", incident=label, folder=folder, problems=tally["problems"])
                    self.check(close_cost(tally["cost_usd"], trajectory.get("info", {}).get("model_stats", {}).get("instance_cost")), "incident_trajectory_cost_mismatch", incident=label, folder=folder)
                    messages = trajectory["messages"]
                    for entry in tally["entries"]:
                        native_id = entry["id"]
                        record = native_map.get(native_id)
                        self.check(record is not None and native_id not in traced, "incident_native_response_missing_or_reused", incident=label, folder=folder, response_id=native_id)
                        traced.add(native_id)
                        if record is None:
                            continue
                        request_id, response = record
                        matched.add(request_id)
                        self.check(response == entry["response"] and self.request_matches(requests[request_id], model, history_input(messages[:entry["message_index"]])), "incident_native_history_mismatch", incident=label, folder=folder, response_id=native_id)
                    prefix = messages[:-1] if messages and messages[-1].get("role") == "exit" else messages
                    for request_id in unissued:
                        if self.request_matches(requests[request_id], model, history_input(prefix)):
                            matched.add(request_id)
                declared = [item for item in receipt.get("models", []) if item.get("model") == model and item.get("folder") == folder]
                count = sum(response.get("model") in accepted and requests[request_id].get("model") == model for request_id, response in native_map.values())
                self.check(len(declared) == 1 and declared[0].get("native_responses") == count and close_cost(declared[0].get("cost_usd"), costs[model], 1e-10), "incident_declared_usage_mismatch", incident=label, folder=folder)
                model_rows.append({"folder": folder, "model": model, "native_responses": count, "traced_native_responses": native_count, "cost_usd": costs[model]})
            unreturned = set(receipt.get("unreturned_native_response_ids", []))
            self.check(set(native_map) - traced == unreturned, "incident_unreturned_response_inventory_mismatch", incident=label)
            for native_id in unreturned:
                if native_id in native_map:
                    matched.add(native_map[native_id][0])
            self.check(matched == set(requests), "incident_request_not_accounted", incident=label, request_ids=sorted(set(requests) - matched))
            self.check(not (set(native_map) & self.used_response_ids), "incident_response_reused_in_official_run", incident=label)
            reports.append({"incident": label, "excluded_from_official_runs": True, "status": receipt["status"], "reason": redact(receipt.get("reason", "")), "models": model_rows,
                            "cost_usd": sum(costs.values()), "native_responses": len(native_map), "unissued_requests": len(unissued), "unreturned_native_response_ids": sorted(unreturned)})
        return reports

    def audit(self):
        manifests = self.preflight()
        baseline = read_json(self.root / "runs/sonnet5.5p30/manifest.json")
        identity = lambda manifest: [{key: task[key] for key in ("case", "version", "interpreter", "hashes")} for task in manifest["tasks"]]
        expected = identity(baseline)
        self.check(len(expected) == 30 and len({task["case"] for task in expected}) == 30, "claude_baseline_not_30_unique")
        baseline_config_hash = read_json(self.root / "runs/sonnet5.5p30/experiment.json")["original_config_sha256"]
        probe_baseline = read_json(self.root / "records/gpt_p30_probe_baseline.json")
        for folder, manifest in manifests.items():
            model, run = MODELS[folder], self.root / "runs" / folder
            self.scan(run / "manifest.json")
            self.check(manifest.get("count") == 30 and identity(manifest) == expected, "selection_differs_from_claude_30", folder=folder)
            self.check(manifest.get("actual_model") == model and manifest.get("mcp_used") is False and manifest.get("candidate_test_feedback") is False, "manifest_model_or_feedback_mismatch", folder=folder)
            accepted_models(model, manifest)
            experiment = read_json(run / "experiment.json")
            self.check(experiment.get("original_config_sha256") == baseline_config_hash == self.digest(self.root / "upstream/configs/apr.yaml"), "upstream_config_hash_changed", folder=folder)
            self.source_freeze(folder, manifest)
            prices = experiment.get("spec", {}).get("prices", manifest.get("prices"))
            if isinstance(prices, list) and len(prices) in {3, 4}:
                prices = dict(zip(("input_per_million", "output_per_million", "cache_read_per_million", "cache_write_per_million"), prices))
            if isinstance(prices, dict):
                prices = {"cache_read_per_million": None, "cache_write_per_million": None} | prices
            usage_cost(prices, {"input_tokens": 0, "output_tokens": 0})
            self.prices[model] = prices
            self.check({key: prices.get(key) for key in PRICES[model]} == PRICES[model] and set(prices) <= set(PRICES[model]) | set(LONG_CONTEXT), "experiment_prices_differ_from_frozen_authorized_rates", folder=folder)
        self.load_queue()
        harness_receipts = self.harness_preflights()
        reports = {}
        for folder, model in MODELS.items():
            manifest, run = manifests[folder], self.root / "runs" / folder
            rows = []
            for task in manifest["tasks"]:
                try:
                    probe = read_json(run / "environment_probes" / task["version"] / "probe.json")
                    baseline_probe = read_json(self.root / "runs/sonnet5.5p30/environment_probes" / task["version"] / "probe.json")
                    self.check(probe.get("qiskit") == task["version"] and probe.get("interpreter") == task["interpreter"] and probe.get("interpreter_sha256") == self.digest(task["interpreter"]), "pinned_interpreter_hash_or_version_changed", folder=folder, case=task["case"])
                    self.check(all(probe.get(key) == baseline_probe.get(key) for key in ("interpreter", "interpreter_sha256", "qiskit", "python")), "interpreter_differs_from_claude", folder=folder, case=task["case"])
                    prepared = probe_baseline["runs"][folder]
                    self.check(prepared.get("runner_sources") == manifest.get("runner_sources") and all(probe.get(key) == prepared["probes"][task["version"]].get(key) for key in ("interpreter", "interpreter_sha256", "qiskit", "python")), "interpreter_or_sources_changed_since_preparation", folder=folder, case=task["case"])
                    rows.append(self.audit_case(folder, model, task))
                except (OSError, ValueError, KeyError, TypeError) as error:
                    self.check(False, "case_audit_failed", folder=folder, case=task["case"], error_type=type(error).__name__, message=redact(str(error)))
            smoke = self.smoke(folder, model)
            report = {"folder": folder, "actual_model": model, "cases_audited": len(rows), "rows": rows, "official_cost_usd": round(sum(row["cost_usd"] for row in rows), 8), "pipeline_smoke": smoke,
                      "native_responses": sum(row["native_responses"] for row in rows), "submitted": sum(row["submitted"] for row in rows), "repaired": sum(row["repaired"] for row in rows), "visible_sensitive_attempts": sum(len(row["visible_attempts"]) for row in rows), "benign_policy_false_positive_count": sum(row["benign_policy_false_positive_count"] for row in rows)}
            report["total_known_usage_cost_usd"] = report["official_cost_usd"] + smoke["cost_usd"]
            summary = read_json(run / "experiment_result.json")
            self.check(close_cost(summary.get("cost_usd"), report["official_cost_usd"], 1e-6) and close_cost(summary.get("pipeline_smoke_cost_usd", 0), smoke["cost_usd"], 1e-6), "exported_cost_totals_mismatch", folder=folder)
            reports[folder] = report
        rows = [row for report in reports.values() for row in report["rows"]]
        self.check(len(rows) == 90, "not_all_90_cases_auditable")
        if rows:
            latest = max(row["agent_phase_end_timestamp"] for row in rows)
            earliest = min(row["estimated_first_test_start_timestamp"] for row in rows)
            self.check(latest <= earliest + 2, "global_final_tests_preceded_completion_of_all_90_agents", latest_generation_end=latest, earliest_final_test=earliest)
            barrier_path = self.root / "records/gpt_p30_generation_barrier.json"
            barrier = read_json(barrier_path)
            barrier_time = datetime.fromisoformat(barrier["created_at"])
            barrier_cases = {(entry["folder"], entry["case"]): entry for entry in barrier.get("cases", [])}
            expected_cases = {(folder, task["case"]) for folder, manifest in manifests.items() for task in manifest["tasks"]}
            self.check(barrier.get("total_cases") == 90 and len(barrier.get("cases", [])) == 90 and set(barrier_cases) == expected_cases, "generation_barrier_case_inventory_mismatch")
            self.check(barrier_time.tzinfo is not None and latest <= barrier_time.timestamp() + 2 and barrier_time.timestamp() <= earliest + 2, "generation_barrier_chronology_invalid")
            for folder, case in expected_cases:
                entry = barrier_cases.get((folder, case), {})
                agent_path = self.root / "runs" / folder / "tasks" / case / "agent_result.json"
                agent = read_json(agent_path)
                self.check(entry.get("agent_result_sha256") == self.digest(agent_path) and entry.get("candidate_sha256") == agent.get("candidate_sha256") and entry.get("finished_at") == agent.get("finished_at"), "agent_result_changed_after_generation_barrier", folder=folder, case=case)
        self.check(not (set(self.response_map) - self.used_response_ids), "native_billed_responses_not_accounted_in_trajectories", response_ids=sorted(set(self.response_map) - self.used_response_ids))
        self.check(set(self.queue_records) == self.claimed_requests, "broker_requests_not_accounted_in_trajectories", request_ids=sorted(set(self.queue_records) - self.claimed_requests))
        queue_cost = Counter()
        for native_id, record in self.response_map.items():
            try:
                requested = record["request"]["model"]
                queue_cost[requested] += usage_cost(self.prices[requested], record["response"]["usage"])
            except (ValueError, KeyError, TypeError):
                self.check(False, "queue_native_usage_invalid", response_id=native_id)
        for folder, model in MODELS.items():
            self.check(close_cost(queue_cost[model], reports[folder]["total_known_usage_cost_usd"], 1e-6), "broker_usage_total_not_reconciled", folder=folder)
        incidents = self.audit_incidents()
        for folder, report in reports.items():
            report["findings"] = [finding for finding in self.findings if finding.get("folder") in (None, folder)]
            report["passed"] = not any(finding["severity"] == "ERROR" for finding in report["findings"])
        return {"schema_version": 1, "audited_at_utc": datetime.now(timezone.utc).isoformat(), "passed": not any(item["severity"] == "ERROR" for item in self.findings), "runs": reports, "findings": self.findings,
                "credential_pattern_findings": self.credentials, "broker_native_responses": len(self.response_map), "broker_request_count": len(self.queue_records), "broker_usage_cost_usd_by_model": dict(queue_cost),
                "excluded_infrastructure_incidents": incidents, "excluded_incident_cost_usd": sum(incident["cost_usd"] for incident in incidents),
                "harness_preflight_receipts": harness_receipts,
                "total_known_usage_cost_usd_including_incidents": sum(queue_cost.values()) + sum(incident["cost_usd"] for incident in incidents),
                "limitations": LIMITATIONS + ["GPT prices are the explicit frozen experiment rates, not a billing invoice.", "Candidate hashes and chronology expose visible post-generation changes; they are not a tamper-proof human-intervention log."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--default-agent-source", type=Path, default=DEFAULT_AGENT_SOURCE)
    parser.add_argument("--write", action="store_true", help="Write only new GPT final_audit.json reports")
    args = parser.parse_args()
    try:
        auditor = Auditor(args.root, args.queue, args.default_agent_source)
        report = auditor.audit()
        if args.write:
            destinations = {auditor.confined(Path("runs") / folder / "final_audit.json"): run for folder, run in report["runs"].items()}
            destinations[auditor.confined("records/gpt_p30_final_audit.json")] = report
            for path, value in destinations.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        print(json.dumps({"passed": report["passed"], "error_count": sum(item["severity"] == "ERROR" for item in report["findings"]), "broker_native_responses": report["broker_native_responses"], "cases_audited": sum(run["cases_audited"] for run in report["runs"].values())}))
        return 0 if report["passed"] else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Audit could not complete: {type(error).__name__}: {redact(str(error))}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
