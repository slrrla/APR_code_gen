"""Read-only provenance audit of completed Claude p30 runs; stdlib only.

No execution, API calls, credential loading, or parsing of reference/test source.
Source and validator files are opened only as bytes for SHA-256 checks. Reports
describe visible artifacts and command attempts, not OS isolation or memorized
training-data leakage. --write writes only final_audit.json report artifacts.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DEFAULT_AGENT_SOURCE = Path("C:/Users/haha9/Desktop/work/APR2/qiskit_apr/.venv/Lib/site-packages/minisweagent/agents/default.py")
MODELS = {"sonnet5.5p30": "claude-sonnet-5-5", "haiku5p30": "claude-haiku-4-5-20251001"}
PRICES = {"claude-sonnet-5-5": (2, 10, 2.5, .2), "claude-haiku-4-5-20251001": (1, 5, 1.25, .1)}
SOURCES = ("buggy.py", "fixed.py", "test.py", "original_question.txt")
HARNESSES = ("claude_p30.py", "claude_model.py", "claude_environment.py", "claude_api_broker.py", "adapter.py")
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
CREDENTIAL = re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}|\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}|\bAKIA[A-Z0-9]{16}\b")
VISIBLE_PATTERNS = {
    "withheld_reference_or_test": re.compile(r"(?:^|[/\\\s'\"])(?:fixed\.py|original\.py|test\.py|validator)(?=$|[/\\\s'\";|&()<>{},])", re.I),
    "prior_run_or_conversation": re.compile(r"(?:^|[/\\\s'\"])(?:codex_p30|sessionlogs?|trajector(?:y|ies)|prior[_-]?runs?|runs)(?:[/\\\s'\"]|$)", re.I),
    "visible_network_or_package_operation": re.compile(r"\b(?:curl|wget|ssh|scp|netcat|telnet|qmcp|pip\d*|conda|mamba|npm|npx)\b|\b(?:import|from)\s+(?:requests|urllib|socket|httpx|aiohttp|anthropic|openai)\b|\bgit\s+(?:clone|fetch|pull|push)\b", re.I),
    "credential_or_protected_config": re.compile(r"\b(?:anthropic_api_key|openai_api_key|aws_secret_access_key|aws_access_key_id)\b|(?:^|[/\\\s'\"])(?:\.env|\.aws|\.ssh|\.codex)(?:[/\\\s'\"]|$)", re.I),
    "parent_traversal": re.compile(r"(?:^|[/\\\s'\"])\.\.(?:[/\\\s'\"]|$)"),
}
LIMITATIONS = [
    "Monitored local processes and heuristic command guards are not an OS filesystem/network sandbox.",
    "Command matches report visible text attempts; they do not prove intent or exclude dynamically constructed access.",
    "Input-field checks cannot prove absence of memorized training-data/reference leakage.",
    "Final-test chronology uses native response timestamps and artifact mtimes with a two-second tolerance; it is not a tamper-proof event log.",
    "API cost is recomputed from recorded native token usage and the experiment's explicit prices, not an invoice.",
]


class IncompleteRunError(ValueError):
    pass


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as error:
        raise ValueError(f"Unreadable JSON artifact: {path.name} ({type(error).__name__})") from None


def redact(text: str) -> str:
    return CREDENTIAL.sub("[REDACTED_CREDENTIAL_PATTERN]", text)


def usage_cost(model: str, usage: dict) -> float:
    """Independent native-usage tally, including billed malformed tool turns."""
    if model not in PRICES or not isinstance(usage, dict):
        raise ValueError("Unsupported model or usage object")
    def count(key, values=usage):
        value = values.get(key, 0)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Invalid native usage count: " + key)
        return value
    if not {"input_tokens", "output_tokens"} <= set(usage):
        raise ValueError("Native usage is missing input/output token counts")
    input_rate, output_rate, write_rate, read_rate = PRICES[model]
    creation = count("cache_creation_input_tokens")
    if "cache_creation" in usage:
        detail = usage["cache_creation"]
        if not isinstance(detail, dict):
            raise ValueError("Invalid cache creation detail")
        five_min = count("ephemeral_5m_input_tokens", detail)
        one_hour = count("ephemeral_1h_input_tokens", detail)
        if five_min + one_hour != creation or one_hour:
            raise ValueError("Inconsistent cache detail or unconfigured one-hour cache pricing")
    return (count("input_tokens") * input_rate + count("output_tokens") * output_rate
            + creation * write_rate + count("cache_read_input_tokens") * read_rate) / 1_000_000


def initial_key(model: str, content) -> str:
    return hashlib.sha256(json.dumps([model, content], sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def visible_classification(command: str, categories: list[str], workspace: Path) -> str:
    """Distinguish literal own-workspace/echo text from a prior-input request."""
    if set(categories) != {"prior_run_or_conversation"}:
        return "visible_sensitive_text"
    lower = command.lower().replace("\\", "/")
    workspace_text = workspace.resolve().as_posix().lower()
    variants = [workspace_text]
    if re.match(r"^[a-z]:/", workspace_text):
        variants.append("/" + workspace_text[0] + workspace_text[2:])
    for variant in variants:
        if variant in lower and not VISIBLE_PATTERNS["prior_run_or_conversation"].search(lower.replace(variant, "")):
            return "own_workspace_path_contains_runs_token"
    echo_text = re.sub(r"\becho\s+(?:\"[^\"]*\bruns\b[^\"]*\"|'[^']*\bruns\b[^']*')", "", lower)
    if echo_text != lower and not VISIBLE_PATTERNS["prior_run_or_conversation"].search(echo_text):
        return "echo_text_contains_runs_word"
    return "visible_sensitive_text"


def capture_probe_baseline(root: Path) -> Path:
    """Preserve preparation-probe metadata before validation overwrites it.

    This is a separate metadata/hash snapshot, not a final audit. Existing
    snapshots are retained. No case source or validator is read here.
    """
    target = root / "claude_p30_probe_baseline.json"
    if target.exists():
        return target
    baseline = {"captured_at_utc": datetime.now(timezone.utc).isoformat(), "runs": {}}
    for folder in MODELS:
        run = root / "runs" / folder
        manifest = read_json(run / "manifest.json")
        probes = {}
        for version in sorted({task["version"] for task in manifest["tasks"]}):
            path = run / "environment_probes" / version / "probe.json"
            probe = read_json(path)
            probes[version] = {key: probe.get(key) for key in ("interpreter", "interpreter_sha256", "qiskit", "python")}
            probes[version]["preparation_probe_mtime_utc"] = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        baseline["runs"][folder] = {"probes": probes, "runner_sources": manifest.get("runner_sources"),
                                     "experiment_status_when_captured": read_json(run / "experiment.json").get("status")}
    target.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def trajectory_usage(trajectory: dict, model: str) -> dict:
    entries, response_ids, times, problems = [], [], [], []
    for message in trajectory.get("messages", []):
        if message.get("role") != "assistant":
            continue
        extra = message.get("extra", {})
        response = extra.get("response")
        if not isinstance(response, dict):
            problems.append("assistant message missing native response")
            continue
        try:
            if response.get("model") != model or response.get("role") != "assistant" or response.get("type") != "message":
                raise ValueError("Native response model/type/role mismatch")
            if extra.get("usage") != response.get("usage") or message.get("content") != response.get("content"):
                raise ValueError("Native content/usage was not retained unchanged")
            cost = usage_cost(model, response["usage"])
            saved_cost = extra.get("cost")
            if isinstance(saved_cost, bool) or not isinstance(saved_cost, (int, float)) or not math.isclose(cost, saved_cost, abs_tol=1e-10):
                raise ValueError("Saved native-turn cost disagrees with usage")
            stamp = extra.get("timestamp")
            if not isinstance(stamp, (int, float)) or not math.isfinite(stamp):
                raise ValueError("Native response timestamp missing/invalid")
            if not isinstance(response.get("id"), str) or not response["id"]:
                raise ValueError("Native response ID missing")
            entries.append({"id": response["id"], "cost_usd": cost, "usage": response["usage"],
                            "has_executable_action": bool(extra.get("actions")), "timestamp": stamp})
            response_ids.append(response["id"])
            times.append(stamp)
        except (KeyError, TypeError, ValueError) as error:
            problems.append(redact(str(error)))
    if len(set(response_ids)) != len(response_ids):
        problems.append("Duplicate native response IDs in trajectory")
    return {"native_responses": len(entries), "cost_usd": sum(entry["cost_usd"] for entry in entries),
            "billed_turns_without_executable_action": sum(not entry["has_executable_action"] for entry in entries),
            "response_ids": response_ids, "last_response_timestamp": max(times, default=0),
            "entries": entries, "problems": problems}


class Auditor:
    def __init__(self, root: Path, queue: Path, default_agent_source: Path):
        self.root, self.queue = root.resolve(), queue.resolve()
        self.default_agent_source = default_agent_source.resolve()
        self.findings, self.credentials, self.queue_records, self.response_map = [], [], {}, {}
        self.digest_cache, self.used_response_ids = {}, set()

    def check(self, passed, code, **evidence):
        if not passed:
            self.findings.append({"severity": "ERROR", "code": code, **evidence})

    def warning(self, code, **evidence):
        self.findings.append({"severity": "WARNING", "code": code, **evidence})

    def validation_adjustment(self, manifest, filename, folder):
        """Accept a byte-preserving final-validator fix only with verifiable scope.

        An unchanged original source snapshot proves all other module-level
        definitions, imports and constants remained identical. This never
        permits repair-agent transport/environment changes during generation.
        """
        receipts = manifest.get("validation_adjustments", [])
        if not isinstance(receipts, list):
            return False
        matches = [item for item in receipts if isinstance(item, dict) and item.get("file") == filename]
        if filename != "adapter.py" or len(matches) != 1:
            return False
        receipt = matches[0]
        try:
            before = Path(receipt["before_source_path"])
            before = (self.root / before).resolve() if not before.is_absolute() else before.resolve()
            before.relative_to(self.root)
            if receipt["before_sha256"] != manifest["runner_sources"][filename] or self.digest(before) != receipt["before_sha256"]:
                return False
            if self.digest(self.root / filename) != receipt["after_sha256"]:
                return False
            allowed_scope = {"validate_task", "snapshot_candidate"}
            if set(receipt["scope_functions"]) not in ({"validate_task"}, allowed_scope) or receipt.get("runtime_environment_unchanged") is not True:
                return False
            applied = datetime.fromisoformat(receipt["applied_at_utc"])
            ended = datetime.fromisoformat(receipt["agent_phase_completed_at_utc"])
            if applied.tzinfo is None or ended.tzinfo is None or applied < ended:
                return False
            old_ast = ast.parse(before.read_text(encoding="utf-8-sig"))
            new_ast = ast.parse((self.root / filename).read_text(encoding="utf-8-sig"))
            def stable_nodes(tree):
                return [ast.dump(node, include_attributes=False) for node in tree.body
                        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name not in set(receipt["scope_functions"])]
            if stable_nodes(old_ast) != stable_nodes(new_ast):
                return False
            self.warning("documented_post_agent_validation_adjustment", folder=folder, file=filename,
                         before_sha256=receipt["before_sha256"], after_sha256=receipt["after_sha256"],
                         applied_at_utc=receipt["applied_at_utc"], agent_phase_completed_at_utc=receipt["agent_phase_completed_at_utc"],
                         scope_functions=receipt["scope_functions"], runtime_environment_ast_unchanged=True,
                         reason=redact(str(receipt.get("reason", ""))))
            return True
        except (OSError, ValueError, KeyError, TypeError, SyntaxError):
            return False

    def digest(self, path):
        path = Path(path)
        if path not in self.digest_cache:
            with path.open("rb") as handle:
                self.digest_cache[path] = hashlib.file_digest(handle, "sha256").hexdigest()
        return self.digest_cache[path]

    def scan(self, path):
        text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
        count = len(CREDENTIAL.findall(text))
        if count:
            self.credentials.append({"file": str(path), "matches": count})
            self.check(False, "credential_pattern_visible", file=str(path), matches=count)

    def preflight(self):
        manifests, missing = {}, []
        for folder in MODELS:
            run = self.root / "runs" / folder
            if not (run / "manifest.json").is_file() or not (run / "experiment.json").is_file():
                missing.append(folder + ": manifest/experiment")
                continue
            manifest = read_json(run / "manifest.json")
            if read_json(run / "experiment.json").get("status") != "complete":
                missing.append(folder + ": experiment not complete")
            for task in manifest.get("tasks", []):
                for filename in ("agent_result.json", "result.json", "traj.json"):
                    if not (run / "tasks" / task["case"] / filename).is_file():
                        missing.append(folder + "/" + task["case"] + "/" + filename)
            manifests[folder] = manifest
        if missing:
            raise IncompleteRunError(f"Final audit requires all completed results ({len(missing)} missing/incomplete; first: {missing[0]})")
        return manifests

    def load_queue(self):
        ready = read_json(self.queue / "ready.json")
        self.check(ready.get("broker_source_sha256") == self.digest(self.root / "claude_api_broker.py"), "broker_ready_hash_mismatch")
        for path in sorted(self.queue.glob("*.request.json")):
            request_id = path.name.removesuffix(".request.json")
            self.scan(path)
            request = read_json(path)
            response_path = self.queue / (request_id + ".response.json")
            record = {"request_id": request_id, "request": request, "request_mtime": path.stat().st_mtime}
            if response_path.is_file():
                self.scan(response_path)
                response = read_json(response_path)
                record.update(response=response, response_mtime=response_path.stat().st_mtime)
                if isinstance(response, dict) and response.get("type") == "message":
                    self.check(response.get("model") == request.get("model"), "queue_model_mismatch", request_id=request_id)
                    native_id = response.get("id")
                    self.check(native_id not in self.response_map, "duplicate_queue_native_response_id", response_id=native_id)
                    self.response_map[native_id] = record
                else:
                    self.warning("broker_error_response", request_id=request_id, error_type=(response.get("error") or {}).get("type"))
            else:
                self.check(False, "queue_response_missing", request_id=request_id)
            self.queue_records[request_id] = record

    def commands(self, trajectory, tdir, folder, case):
        path = tdir / "command_audit/commands.jsonl"
        self.scan(path)
        events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        results = [event for event in events if event.get("event") == "result"]
        final = {(event.get("session_id"), event.get("id")): event for event in results}
        attempts = [event for event in events if event.get("event") == "attempt"]
        self.check(len(final) == len(attempts), "command_attempt_without_final_result", folder=folder, case=case)
        serialized = trajectory.get("environment_commands", [])
        self.check(serialized == [{k: v for k, v in event.items() if k != "event"} for event in results],
                   "trajectory_command_audit_mismatch", folder=folder, case=case)
        visible = []
        for attempt in attempts:
            command = attempt.get("command", "")
            categories = [name for name, pattern in VISIBLE_PATTERNS.items() if pattern.search(command)]
            if not categories:
                continue
            result = final.get((attempt.get("session_id"), attempt.get("id")), {})
            status = result.get("status", "MISSING_RESULT")
            item = {"case": case, "command_id": attempt.get("id"), "categories": categories,
                    "status": status, "guard_reasons": result.get("guard_reasons", []),
                    "classification": visible_classification(command, categories, tdir / "workspace"),
                    "command_sha256": hashlib.sha256(command.encode()).hexdigest(), "command_excerpt": redact(command[:1000])}
            item["visible_guard_false_positive"] = status == "POLICY_REJECTED" and item["classification"] != "visible_sensitive_text"
            if item["visible_guard_false_positive"]:
                item["classification_reason"] = item["classification"]
                item["classification"] = "benign_policy_false_positive"
            visible.append(item)
            if item["visible_guard_false_positive"]:
                self.warning("benign_policy_false_positive", folder=folder, **item)
            elif status != "POLICY_REJECTED" and item["classification"] == "visible_sensitive_text":
                self.warning("visible_sensitive_command_not_policy_rejected", folder=folder, **item)
        return {"status_counts": dict(Counter(event.get("status") for event in results)),
                "visible_attempts": visible, "benign_policy_false_positive_count": sum(item["visible_guard_false_positive"] for item in visible),
                "submitted_commands": sum(event.get("status") == "SUBMITTED" for event in results)}

    def audit_case(self, folder, model, task):
        case, version = task["case"], task["version"]
        tdir = self.root / "runs" / folder / "tasks" / case
        context, agent, result, trajectory = [read_json(tdir / name) for name in
                                           ("agent_input.json", "agent_result.json", "result.json", "traj.json")]
        for filename in ("agent_input.json", "agent_result.json", "result.json", "traj.json"):
            self.scan(tdir / filename)
        self.check(set(context) == {"case", "version", "title", "question"}, "unexpected_initial_input_fields", folder=folder, case=case)
        self.check(context.get("case") == case and context.get("version") == version, "initial_input_identity_mismatch", folder=folder, case=case)
        self.check(not re.search(r"(?im)^\s*(?:Solution explanation|Original fixed code|Answer):", context.get("question", "")),
                   "solution_section_in_initial_question", folder=folder, case=case)
        self.check(all(agent.get(key) == expected for key, expected in (("case", case), ("version", version), ("model", model))),
                   "agent_identity_mismatch", folder=folder, case=case)
        source = Path(task["source_dir"]).resolve()
        if source != (self.root.parent / case).resolve():
            raise ValueError("Original source directory is outside the selected case directory")
        self.check(set(task["hashes"]) == set(SOURCES), "unexpected_source_hash_fields", folder=folder, case=case)
        for filename in SOURCES:
            self.check(self.digest(source / filename) == task["hashes"].get(filename), "original_source_hash_changed", folder=folder, case=case, filename=filename)
        present = agent.get("candidate_present", True)
        if present is False:
            self.check(not (tdir / "workspace/buggy.py").exists() and agent.get("candidate_sha256") == EMPTY_SHA256
                       and (tdir / "patched.py").stat().st_size == 0 and result.get("candidate_missing") is True
                       and result.get("repaired") is False and agent.get("submitted") is False,
                       "deleted_candidate_not_consistently_recorded_as_failure", folder=folder, case=case)
        else:
            self.check(present is True and self.digest(tdir / "workspace/buggy.py") == agent.get("candidate_sha256"),
                       "workspace_candidate_hash_changed", folder=folder, case=case)
            self.check(result.get("candidate_missing", False) is False, "present_candidate_marked_missing", folder=folder, case=case)
        for relative, expected in (("original.py", task["hashes"]["buggy.py"]), ("validator/test.py", task["hashes"]["test.py"]),
                                   ("patched.py", agent.get("candidate_sha256"))):
            self.check(self.digest(tdir / relative) == expected, "snapshot_or_candidate_hash_changed", folder=folder, case=case, filename=relative)
        for variant, expected in (("original", task["hashes"]["buggy.py"]), ("reference", task["hashes"]["fixed.py"]), ("candidate", agent.get("candidate_sha256"))):
            record = result.get(variant, {})
            self.check(record.get("source_sha256") == expected and record.get("test_sha256") == task["hashes"]["test.py"],
                       "tested_source_or_test_hash_mismatch", folder=folder, case=case, variant=variant)
        info = trajectory.get("info", {})
        messages = trajectory.get("messages", [])
        self.check(bool(messages) and messages[-1].get("role") == "exit", "trajectory_not_closed_with_exit_message", folder=folder, case=case)
        cfg = info.get("config", {})
        self.check(cfg.get("agent_type") == "minisweagent.agents.default.DefaultAgent", "native_agent_type_mismatch", folder=folder, case=case)
        self.check(cfg.get("model", {}).get("model_name") == model, "trajectory_model_config_mismatch", folder=folder, case=case)
        self.check(all(cfg.get("agent", {}).get(key) == expected for key, expected in
                       (("step_limit", 40), ("cost_limit", 1), ("wall_time_limit_seconds", 1200))), "native_budget_mismatch", folder=folder, case=case)
        tally = trajectory_usage(trajectory, model)
        for problem in tally["problems"]:
            self.check(False, "native_trajectory_integrity", folder=folder, case=case, problem=problem)
        stats = info.get("model_stats", {})
        self.check(math.isclose(tally["cost_usd"], agent.get("cost_usd", -1), abs_tol=1e-8)
                   and math.isclose(tally["cost_usd"], stats.get("instance_cost", -1), abs_tol=1e-8), "trajectory_cost_mismatch", folder=folder, case=case)
        self.check(stats.get("api_calls") == agent.get("steps") and tally["native_responses"] <= agent.get("steps", -1), "trajectory_call_count_mismatch", folder=folder, case=case)
        if agent.get("exit_status") == "LimitsExceeded":
            self.check(agent.get("steps", 0) >= 40 or tally["cost_usd"] >= 1,
                       "limit_exit_without_native_step_or_cost_limit", folder=folder, case=case)
        if tally["native_responses"] < agent.get("steps", 0):
            self.warning("model_calls_without_saved_native_response", folder=folder, case=case, missing=agent["steps"] - tally["native_responses"])
        initial_users = [message for message in trajectory.get("messages", []) if message.get("role") == "user"]
        first_content = initial_users[0].get("content") if initial_users else None
        self.check(isinstance(first_content, str) and context.get("question", "") in first_content, "initial_prompt_missing_sanitized_question", folder=folder, case=case)
        request_times, response_times = [], []
        for entry in tally["entries"]:
            record = self.response_map.get(entry["id"])
            self.check(record is not None, "native_response_missing_from_broker_queue", folder=folder, case=case, response_id=entry["id"])
            if not record:
                continue
            self.used_response_ids.add(entry["id"])
            saved = next(message["extra"]["response"] for message in trajectory["messages"]
                         if message.get("extra", {}).get("response", {}).get("id") == entry["id"])
            self.check(record["response"] == saved, "broker_response_differs_from_trajectory", folder=folder, case=case, response_id=entry["id"])
            request = record["request"]
            request_first = request.get("messages", [{}])[0].get("content")
            self.check(request.get("model") == model and initial_key(model, request_first) == initial_key(model, first_content),
                       "broker_request_initial_input_mismatch", folder=folder, case=case, response_id=entry["id"])
            request_times.append(record["request_mtime"])
            response_times.append(record["response_mtime"])
        command_report = self.commands(trajectory, tdir, folder, case)
        submitted = agent.get("exit_status") == "Submitted"
        self.check(agent.get("submitted") == submitted and info.get("exit_status") == agent.get("exit_status")
                   and command_report["submitted_commands"] == int(submitted), "submission_records_disagree", folder=folder, case=case)
        self.check(agent.get("candidate_test_feedback") is False, "candidate_test_feedback_flag_changed", folder=folder, case=case)
        test_starts = []
        for variant in ("original", "reference", "candidate"):
            log = read_json(tdir / "logs" / (variant + ".json"))
            output = tdir / "logs" / (variant + ".stdout.txt")
            # execute_test writes stdout after execution; subtract its recorded
            # duration for a conservative approximation of the start time.
            test_starts.append(output.stat().st_mtime - log["seconds"])
        # DefaultAgent saves the closed trajectory when its final exit message
        # is recorded. agent_result.json may be created much later by recovery
        # or finalization and cannot represent when model execution stopped.
        end = max([tally["last_response_timestamp"], (tdir / "traj.json").stat().st_mtime, *request_times, *response_times])
        self.check(end <= min(test_starts) + 2, "final_test_started_before_agent_phase_ended", folder=folder, case=case)
        return {"case": case, "version": version, "native_responses": tally["native_responses"],
                "billed_turns_without_executable_action": tally["billed_turns_without_executable_action"],
                "cost_usd": round(tally["cost_usd"], 10), "submitted": submitted,
                "generated_test_status": result["candidate"]["status"], "repaired": result["repaired"], "candidate_present": present,
                "last_native_response_timestamp": tally["last_response_timestamp"],
                "agent_phase_end_timestamp": end, "estimated_first_test_start_timestamp": min(test_starts), **command_report}

    def smoke(self, folder, model):
        directory = self.root / "runs" / folder / "pipeline_smoke"
        items = []
        for path in sorted(directory.glob("*/agent_result.json")):
            self.scan(path)
            agent = read_json(path)
            trajectory_path = path.with_name("traj.json")
            if trajectory_path.is_file():
                self.scan(trajectory_path)
                tally = trajectory_usage(read_json(trajectory_path), model)
                self.check(not tally["problems"] and math.isclose(tally["cost_usd"], agent["cost_usd"], abs_tol=1e-8),
                           "pipeline_smoke_usage_cost_mismatch", folder=folder, case=path.parent.name)
                for native_id in tally["response_ids"]:
                    self.check(native_id in self.response_map, "pipeline_smoke_response_missing_from_queue", folder=folder, response_id=native_id)
                    self.used_response_ids.add(native_id)
                items.append({"case": path.parent.name, "cost_usd": tally["cost_usd"], "native_responses": tally["native_responses"]})
            else:
                self.check(False, "pipeline_smoke_trajectory_missing", folder=folder, case=path.parent.name)
        return {"cases": items, "cost_usd": sum(item["cost_usd"] for item in items), "separate_from_official_30_case_budget": True}

    def audit(self):
        manifests = self.preflight()
        self.load_queue()
        original = read_json(self.root / "runs/codex_p30/manifest.json")
        def identity(manifest):
            return [{key: task[key] for key in ("case", "version", "interpreter", "hashes")} for task in manifest["tasks"]]
        expected = identity(original)
        self.check(len(expected) == 30 and len({task["case"] for task in expected}) == 30, "original_selection_not_30_unique")
        reports = {}
        baseline_path = self.root / "claude_p30_probe_baseline.json"
        baseline = read_json(baseline_path) if baseline_path.exists() else None
        if baseline is None:
            self.warning("preparation_interpreter_hash_baseline_missing", limitation="Current hash versus final probe alone does not establish stability since preparation")
        for folder, model in MODELS.items():
            run, manifest = self.root / "runs" / folder, manifests[folder]
            start_findings = len(self.findings)
            self.scan(run / "manifest.json")
            self.scan(run / "experiment.json")
            self.check(manifest.get("count") == 30 and identity(manifest) == expected, "selection_differs_from_original_30", folder=folder)
            self.check(manifest.get("actual_model") == model and manifest.get("candidate_test_feedback") is False and manifest.get("mcp_used") is False,
                       "manifest_model_or_feedback_mismatch", folder=folder)
            sources = manifest.get("runner_sources", {})
            for filename in HARNESSES:
                same = sources.get(filename) == self.digest(self.root / filename)
                self.check(same or self.validation_adjustment(manifest, filename, folder), "harness_source_hash_changed", folder=folder, filename=filename)
            self.check(manifest.get("default_agent_source_sha256") == self.digest(self.default_agent_source), "default_agent_source_hash_changed", folder=folder)
            experiment = read_json(run / "experiment.json")
            self.check(experiment.get("original_config_sha256") == self.digest(self.root / "upstream/configs/apr.yaml"), "upstream_config_hash_changed", folder=folder)
            rows = []
            for task in manifest["tasks"]:
                try:
                    probe = read_json(run / "environment_probes" / task["version"] / "probe.json")
                    self.check(probe.get("qiskit") == task["version"] and probe.get("interpreter") == task["interpreter"]
                               and probe.get("interpreter_sha256") == self.digest(task["interpreter"]), "pinned_interpreter_hash_or_version_changed", folder=folder, case=task["case"])
                    if baseline is not None:
                        prepared = baseline["runs"][folder]["probes"][task["version"]]
                        self.check(all(prepared.get(key) == probe.get(key) for key in ("interpreter", "interpreter_sha256", "qiskit", "python")),
                                   "interpreter_preparation_baseline_changed", folder=folder, case=task["case"])
                        self.check(baseline["runs"][folder].get("runner_sources") == sources, "probe_baseline_harness_identity_changed", folder=folder)
                    rows.append(self.audit_case(folder, model, task))
                except (OSError, ValueError, KeyError, TypeError) as error:
                    self.check(False, "case_audit_failed", folder=folder, case=task["case"], error_type=type(error).__name__, message=redact(str(error)))
            smoke = self.smoke(folder, model)
            report = {"folder": folder, "actual_model": model, "cases_audited": len(rows), "rows": rows,
                      "official_cost_usd": round(sum(row["cost_usd"] for row in rows), 8), "pipeline_smoke": smoke,
                      "native_responses": sum(row["native_responses"] for row in rows),
                      "submitted": sum(row["submitted"] for row in rows), "repaired": sum(row["repaired"] for row in rows),
                      "visible_sensitive_attempts": sum(len(row["visible_attempts"]) for row in rows),
                      "benign_policy_false_positive_count": sum(row["benign_policy_false_positive_count"] for row in rows),
                      "findings": self.findings[start_findings:], "limitations": LIMITATIONS}
            report["total_known_usage_cost_usd"] = round(report["official_cost_usd"] + smoke["cost_usd"], 8)
            summary = read_json(run / "experiment_result.json")
            self.check(math.isclose(summary.get("cost_usd", -1), report["official_cost_usd"], abs_tol=1e-6)
                       and math.isclose(summary.get("pipeline_smoke_cost_usd", -1), smoke["cost_usd"], abs_tol=1e-6), "exported_cost_totals_mismatch", folder=folder)
            reports[folder] = report
        all_rows = [row for report in reports.values() for row in report["rows"]]
        if len(all_rows) == 60:
            self.check(max(row["agent_phase_end_timestamp"] for row in all_rows) <= min(row["estimated_first_test_start_timestamp"] for row in all_rows) + 2,
                       "global_final_tests_preceded_completion_of_all_60_agents")
            for folder, manifest in manifests.items():
                for receipt in manifest.get("validation_adjustments", []):
                    if isinstance(receipt, dict) and receipt.get("file") == "adapter.py":
                        try:
                            ended = datetime.fromisoformat(receipt["agent_phase_completed_at_utc"]).timestamp()
                            latest_native = max(row["last_native_response_timestamp"] for row in all_rows)
                            self.check(latest_native <= ended + 2, "validation_adjustment_preceded_native_agent_completion", folder=folder)
                        except (ValueError, KeyError, TypeError):
                            self.check(False, "validation_adjustment_timestamp_invalid", folder=folder)
        orphan = set(self.response_map) - self.used_response_ids
        self.check(not orphan, "native_billed_responses_not_accounted_in_official_or_smoke_trajectories", response_ids=sorted(orphan))
        queue_cost = Counter()
        for native_id, record in self.response_map.items():
            try:
                response = record["response"]
                queue_cost[response["model"]] += usage_cost(response["model"], response["usage"])
            except (KeyError, TypeError, ValueError):
                self.check(False, "queue_native_usage_invalid", response_id=native_id)
        for model in MODELS.values():
            traced = sum(report["total_known_usage_cost_usd"] for report in reports.values() if report["actual_model"] == model)
            self.check(math.isclose(queue_cost[model], traced, abs_tol=1e-6), "broker_usage_total_not_reconciled", model=model)
        for folder, report in reports.items():
            report["findings"] = [finding for finding in self.findings if finding.get("folder") in (None, folder)]
            report["passed"] = not any(finding["severity"] == "ERROR" for finding in report["findings"])
        result = {"schema_version": 1, "audited_at_utc": datetime.now(timezone.utc).isoformat(),
                  "passed": not any(item["severity"] == "ERROR" for item in self.findings), "runs": reports,
                  "findings": self.findings, "credential_pattern_findings": self.credentials,
                  "broker_native_responses": len(self.response_map), "broker_request_count": len(self.queue_records),
                  "broker_usage_cost_usd_by_model": {model: round(cost, 8) for model, cost in queue_cost.items()}, "limitations": LIMITATIONS}
        result["preparation_probe_baseline_captured_at_utc"] = baseline.get("captured_at_utc") if baseline else None
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--default-agent-source", type=Path, default=DEFAULT_AGENT_SOURCE)
    parser.add_argument("--write", action="store_true", help="Save completed per-run and comparison final_audit.json reports")
    parser.add_argument("--capture-probes", action="store_true", help="Only preserve preparation-probe metadata before final validation; do not perform a final audit")
    args = parser.parse_args()
    if args.capture_probes:
        print(str(capture_probe_baseline(args.root.resolve())))
        return 0
    auditor = Auditor(args.root, args.queue or args.root / "api_queue", args.default_agent_source)
    try:
        report = auditor.audit()
    except IncompleteRunError as error:
        print(str(error))
        return 2
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Audit could not complete: {type(error).__name__}: {redact(str(error))}")
        return 2
    if args.write:
        for folder, run_report in report["runs"].items():
            (args.root / "runs" / folder / "final_audit.json").write_text(json.dumps(run_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.root / "claude_p30_final_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "error_count": sum(item["severity"] == "ERROR" for item in report["findings"]),
                      "warning_count": sum(item["severity"] == "WARNING" for item in report["findings"]),
                      "runs": {folder: {key: run[key] for key in ("cases_audited", "native_responses", "official_cost_usd", "submitted", "repaired", "visible_sensitive_attempts", "benign_policy_false_positive_count")} for folder, run in report["runs"].items()}}, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
