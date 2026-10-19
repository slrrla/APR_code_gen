"""Offline synthetic provenance contracts; no API calls or benchmark execution."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from jinja2 import StrictUndefined, Template
import yaml

import audit_gpt_runs as audit


TEMP_ROOT = Path(__file__).resolve().parent.parent / "records/gpt_p30_test_tmp"


def write(path, value, stamp=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    if stamp is not None:
        os.utime(path, (stamp, stamp))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iso(stamp):
    return datetime.fromtimestamp(stamp, timezone.utc).isoformat()


def native_response(model, identifier, stamp):
    return {"id": identifier, "object": "response", "model": model, "status": "completed", "created_at": int(stamp),
            "output": [{"type": "function_call", "id": "fc_" + identifier, "call_id": "call_" + identifier,
                        "name": "bash", "status": "completed", "arguments": json.dumps({"command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"})}],
            "usage": {"input_tokens": 100, "output_tokens": 10, "total_tokens": 110,
                      "input_tokens_details": {"cached_tokens": 20}, "output_tokens_details": {"reasoning_tokens": 5}}}


class AuditContracts(unittest.TestCase):
    def fixture(self, base):
        root = base / "cases/apr_p30"
        root.mkdir(parents=True)
        queue = audit.default_queue_path(root)
        queue.mkdir(parents=True)
        tools, snapshots = root / "tools", root / "records/gpt_p30_sources"
        tools.mkdir()
        snapshots.mkdir()
        for name in audit.HARNESSES:
            (tools / name).write_bytes(b"synthetic unexecuted harness bytes")
            (snapshots / name).write_bytes((tools / name).read_bytes())
        default_source = root / "default_agent.py"
        default_source.write_bytes(b"synthetic DefaultAgent bytes; never imported")
        (snapshots / "default.py").write_bytes(default_source.read_bytes())
        interpreter = root / "python.exe"
        interpreter.write_bytes(b"synthetic interpreter; never executed")
        config = root / "upstream/configs/apr.yaml"
        config.parent.mkdir(parents=True)
        original_config = {"agent": {"system_template": "Synthetic Qiskit expert\n", "instance_template": "Repair /work/buggy.py for {{qiskit_version}}\n{{title}}\nError: {{error_text}}\n{% if mcp_enabled %}MCP{% endif %}\n",
                                     "step_limit": 40, "cost_limit": 1.0, "wall_time_limit_seconds": 1200},
                           "model": {"observation_template": "{{output.output}}", "format_error_template": "{{error}}"}}
        config.write_text(yaml.safe_dump(original_config), encoding="utf-8")
        (snapshots / "apr.yaml").write_bytes(config.read_bytes())
        agent_config = original_config["agent"] | {"max_consecutive_format_errors": 3}
        agent_config["instance_template"] = agent_config["instance_template"].replace("/work/buggy.py", "buggy.py") + audit.QUESTION_APPENDIX
        stamp = time.time() - 1000
        health = root / "records/gpt_p30_harness_preflight/synthetic/1.2.3/command_audit"
        health.mkdir(parents=True)
        (health / "stdout.txt").write_bytes(b"731942\r\n")
        (health / "commands.jsonl").write_text(json.dumps({"event": "result", "command": '$PY -c "print(731942)"', "status": "EXECUTED", "returncode": 0, "stdout_log": str(health / "stdout.txt")}) + "\n", encoding="utf-8")
        write(health.parent.parent / "receipt.json", {"checked_at": iso(stamp - 20), "checks": [{"version": "1.2.3", "returncode": 0, "passed": True}]})
        selected = []
        for index in range(30):
            case = f"issue_{index:03}"
            source = root.parent / case
            source.mkdir()
            for name in audit.SOURCES:
                (source / name).write_bytes(("synthetic " + name + case).encode())
            selected.append({"case": case, "version": "1.2.3", "interpreter": str(interpreter), "source_dir": str(source),
                             "hashes": {name: digest(source / name) for name in audit.SOURCES}})
            baseline = root / "runs/sonnet5.5p30/tasks" / case
            write(baseline / "agent_input.json", {"case": case, "version": "1.2.3", "title": "Synthetic " + case, "question": "Synthetic question " + case})
            write(baseline / "traj.json", {"info": {"config": {"agent": agent_config | {"output_path": "old Claude path"}}}})
        write(root / "runs/sonnet5.5p30/manifest.json", {"count": 30, "tasks": selected, "default_agent_source_sha256": digest(default_source), "runner_sources": {name: digest(tools / name) for name in audit.HARNESSES}})
        write(root / "runs/sonnet5.5p30/experiment.json", {"status": "complete", "original_config_sha256": digest(config)})
        probe = {"qiskit": "1.2.3", "interpreter": str(interpreter), "interpreter_sha256": digest(interpreter), "python": "3.synthetic"}
        write(root / "runs/sonnet5.5p30/environment_probes/1.2.3/probe.json", probe)
        write(queue / "startup.json", {"ready": True, "preflight_ok": True, "allowed_models": list(audit.MODELS.values()),
                                      "broker_source_sha256": digest(tools / "openai_api_broker.py"),
                                      "accepted_response_models": {model: [model] for model in audit.MODELS.values()}})
        barrier = {"created_at": iso(stamp + 20), "total_cases": 90, "cases": []}
        probe_baseline = {"captured_at_utc": iso(stamp - 10), "runs": {}}
        for folder, model in audit.MODELS.items():
            run, prices = root / "runs" / folder, audit.PRICES[model]
            write(run / "manifest.json", {"count": 30, "tasks": selected, "actual_model": model, "accepted_response_models": [model],
                                          "candidate_test_feedback": False, "mcp_used": False, "mini_swe_version": "2.4.6",
                                          "runner_sources": {name: digest(tools / name) for name in audit.HARNESSES},
                                          "source_snapshot_directory": "records/gpt_p30_sources", "default_agent_source_sha256": digest(default_source)})
            write(run / "experiment.json", {"status": "complete", "spec": {"prices": prices}, "original_config_sha256": digest(config)})
            write(run / "environment_probes/1.2.3/probe.json", probe)
            probe_baseline["runs"][folder] = {"probes": {"1.2.3": probe}, "runner_sources": {name: digest(tools / name) for name in audit.HARNESSES}}
            total_cost = 0
            for index, task in enumerate(selected):
                case = task["case"]
                tdir = run / "tasks" / case
                context = audit.read_json(root / "runs/sonnet5.5p30/tasks" / case / "agent_input.json")
                write(tdir / "agent_input.json", context)
                (tdir / "original.py").write_bytes((Path(task["source_dir"]) / "buggy.py").read_bytes())
                validator = tdir / "validator/test.py"
                validator.parent.mkdir()
                validator.write_bytes((Path(task["source_dir"]) / "test.py").read_bytes())
                candidate = tdir / "workspace/buggy.py"
                candidate.parent.mkdir()
                candidate.write_bytes(b"synthetic repaired bytes; never executed")
                (tdir / "patched.py").write_bytes(candidate.read_bytes())
                response = native_response(model, "resp_" + folder + case, stamp)
                cost = audit.usage_cost(prices, response["usage"])
                total_cost += cost
                out = tdir / "command_audit/reproduction.stdout.txt"
                out.parent.mkdir()
                out.write_bytes(b"Synthetic initial exception\r\n")
                common = {"session_id": "synthetic-session", "time_utc": iso(stamp), "seconds": .01}
                commands = [common | {"id": 1, "command": "$PY buggy.py", "status": "EXECUTED", "returncode": 1, "stdout_log": str(out)},
                            common | {"id": 2, "command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT", "status": "SUBMITTED", "returncode": 0}]
                variables = dict(task="", title=context["title"], question=context["question"], qiskit_version="1.2.3", error_text=out.read_bytes().decode(), mcp_enabled=False)
                messages = [{"role": role, "content": Template(agent_config[key], undefined=StrictUndefined).render(**variables)}
                            for role, key in (("system", "system_template"), ("user", "instance_template"))]
                first_messages = deepcopy(messages)
                messages += [{"role": "assistant", "content": response["output"],
                              "extra": {"response": response, "usage": response["usage"], "cost": cost, "cost_status": "priced", "timestamp": stamp,
                                        "actions": [{"command": commands[1]["command"], "tool_call_id": response["output"][0]["call_id"]}]}},
                             {"role": "exit", "content": "", "extra": {"exit_status": "Submitted"}}]
                trajectory = {"info": {"exit_status": "Submitted", "mini_version": "2.4.6", "model_stats": {"instance_cost": cost, "api_calls": 1},
                                        "config": {"agent_type": "minisweagent.agents.default.DefaultAgent", "agent": agent_config | {"output_path": str(tdir / "traj.json")},
                                                   "model_type": "openai_model.OpenAIResponsesModel", "environment_type": "claude_environment.MonitoredBashEnvironment",
                                                   "model": original_config["model"] | {"model_name": model, "max_tokens": 8192, "model_kwargs": {}, "reasoning_policy": "provider_default", "prices": prices | audit.LONG_CONTEXT, "accepted_response_models": [model]}}},
                              "messages": messages, "environment_commands": commands}
                write(tdir / "traj.json", trajectory, stamp + 1)
                agent = {"case": case, "version": "1.2.3", "model": model, "exit_status": "Submitted", "submitted": True,
                         "steps": 1, "cost_usd": cost, "candidate_test_feedback": False, "candidate_sha256": digest(candidate), "candidate_present": True, "started_at": iso(stamp - 2), "finished_at": iso(stamp + 2), "native_responses": 1, "cost_statuses": ["priced"]}
                write(tdir / "agent_result.json", agent, stamp + 2)
                barrier["cases"].append({"folder": folder, "case": case, "agent_result_sha256": digest(tdir / "agent_result.json"), "candidate_sha256": agent["candidate_sha256"], "finished_at": agent["finished_at"]})
                events = []
                for command in commands:
                    events.extend([{"event": "attempt", **{key: value for key, value in command.items() if key not in {"status", "seconds"}}}, {"event": "result", **command}])
                (out.parent / "commands.jsonl").write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
                result = {"case": case, "version": "1.2.3", "baseline_valid": True, "candidate_missing": False, "repaired": True,
                          "audit": {"changed": True, "syntax_ok": True, "suspicious": False}}
                for variant, source_hash in (("original", task["hashes"]["buggy.py"]), ("reference", task["hashes"]["fixed.py"]), ("candidate", digest(candidate))):
                    record = {"status": "FAIL" if variant == "original" else "PASS", "source_sha256": source_hash, "test_sha256": task["hashes"]["test.py"], "interpreter": str(interpreter), "tests_run": 1, "skipped": 0, "seconds": .1}
                    result[variant] = record
                    write(tdir / "logs" / (variant + ".json"), record)
                    output = tdir / "logs" / (variant + ".stdout.txt")
                    output.write_bytes(b"synthetic final output; never parsed")
                    os.utime(output, (stamp + 30, stamp + 30))
                write(tdir / "result.json", result)
                request_id = hashlib.md5((folder + case).encode()).hexdigest()
                request = {"model": model, "input": first_messages, "tools": [audit.BASH_TOOL], "tool_choice": "auto", "parallel_tool_calls": False, "max_output_tokens": 8192, "store": False, "include": ["reasoning.encrypted_content"]}
                write(queue / (request_id + ".request.json"), request, stamp - 1)
                write(queue / (request_id + ".claimed.json"), {"claimed": True, "model": model, "claimed_at": iso(stamp - .5)}, stamp - .5)
                write(queue / (request_id + ".response.json"), response, stamp)
            write(run / "experiment_result.json", {"cost_usd": total_cost, "pipeline_smoke_cost_usd": 0})
        write(root / "records/gpt_p30_generation_barrier.json", barrier, stamp + 20)
        write(root / "records/gpt_p30_probe_baseline.json", probe_baseline, stamp - 10)
        return root, queue, default_source

    def temporary(self):
        TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        return tempfile.TemporaryDirectory(dir=TEMP_ROOT)

    def incident_fixture(self, root):
        incident = root / "records/gpt_p30_environment_failure_01"
        queue = incident / "records/gpt_p30_api_queue"
        snapshot = incident / "records/gpt_p30_sources/openai_api_broker.py"
        snapshot.parent.mkdir(parents=True)
        snapshot.write_bytes(b"synthetic interrupted broker source; never executed")
        write(queue / "startup.json", {"broker_source_sha256": digest(snapshot)})
        receipt = {"excluded_from_official_runs": True, "status": "infrastructure_interrupted", "reason": "Synthetic shell startup failure", "models": [], "unreturned_native_response_ids": [], "unanswered_requests": []}
        for folder, model in audit.MODELS.items():
            run = incident / "runs" / folder
            write(run / "manifest.json", {"accepted_response_models": [model], "runner_sources": {"openai_api_broker.py": digest(snapshot)}})
            response = native_response(model, "incident_" + folder, time.time())
            cost = audit.usage_cost(audit.PRICES[model], response["usage"])
            messages = [{"role": "system", "content": "Synthetic"}, {"role": "user", "content": "Synthetic initial prompt"}]
            request_id = hashlib.md5(("incident_" + folder).encode()).hexdigest()
            common = {"model": model, "tools": [audit.BASH_TOOL], "tool_choice": "auto", "parallel_tool_calls": False, "max_output_tokens": 8192, "store": False, "include": ["reasoning.encrypted_content"]}
            write(queue / (request_id + ".request.json"), common | {"input": deepcopy(messages)})
            write(queue / (request_id + ".claimed.json"), {"claimed": True, "model": model})
            write(queue / (request_id + ".response.json"), response)
            messages.append({"role": "assistant", "content": response["output"], "extra": {"response": response, "usage": response["usage"], "cost": cost, "cost_status": "priced", "timestamp": time.time(), "actions": [{"command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT", "tool_call_id": response["output"][0]["call_id"]}]}})
            messages.append({"role": "user", "content": [{"type": "function_call_output", "call_id": response["output"][0]["call_id"], "output": "Shell failed to start"}]})
            write(run / "tasks/issue_000/traj.json", {"messages": messages, "info": {"model_stats": {"instance_cost": cost, "api_calls": 1}}})
            unissued_id = hashlib.md5(("unissued_" + folder).encode()).hexdigest()
            write(queue / (unissued_id + ".request.json"), common | {"input": audit.history_input(messages)})
            receipt["models"].append({"folder": folder, "model": model, "native_responses": 1, "cost_usd": cost})
            receipt["unanswered_requests"].append({"request_id": unissued_id, "claimed": False})
        write(incident / "incident.json", receipt)
        inventory = {path.relative_to(incident).as_posix(): {"sha256": digest(path), "bytes": path.stat().st_size, "mtime_ns": path.stat().st_mtime_ns} for path in incident.rglob("*") if path.is_file()}
        write(incident / "archive_index.json", {"files": inventory})
        return incident

    def test_all_90_native_runs_reconcile_and_audit_is_read_only(self):
        with self.temporary() as temp:
            root, queue, source = self.fixture(Path(temp))
            self.incident_fixture(root)
            before = {path: (digest(path), path.stat().st_mtime_ns) for path in root.rglob("*") if path.is_file()}
            report = audit.Auditor(root, queue, source).audit()
            self.assertTrue(report["passed"], report["findings"])
            self.assertEqual(report["broker_native_responses"], 90)
            self.assertEqual(sum(run["cases_audited"] for run in report["runs"].values()), 90)
            self.assertEqual(report["runs"]["gpt6astrap30"]["official_cost_usd"], .0396)
            self.assertEqual(report["excluded_infrastructure_incidents"][0]["native_responses"], 3)
            self.assertEqual(report["excluded_infrastructure_incidents"][0]["unissued_requests"], 3)
            self.assertGreater(report["total_known_usage_cost_usd_including_incidents"], sum(report["broker_usage_cost_usd_by_model"].values()))
            self.assertEqual(before, {path: (digest(path), path.stat().st_mtime_ns) for path in root.rglob("*") if path.is_file()})

    def test_interrupted_cohort_index_detects_any_artifact_change(self):
        with self.temporary() as temp:
            root = Path(temp)
            incident = self.incident_fixture(root)
            source = next((incident / "records/gpt_p30_api_queue").glob("*.response.json"))
            source.write_bytes(source.read_bytes() + b"\n")
            auditor = audit.Auditor(root)
            result = auditor.audit_incidents()
            self.assertEqual(result[0]["native_responses"], 3)
            self.assertIn("incident_archive_file_changed", {finding["code"] for finding in auditor.findings})

    def test_incomplete_run_stops_before_hashing_any_source(self):
        with self.temporary() as temp:
            root, queue, source = self.fixture(Path(temp))
            (root / "runs/gpt6solp30/tasks/issue_029/result.json").unlink()
            with patch.object(audit.Auditor, "digest", side_effect=AssertionError("No source reads before completion")):
                with self.assertRaises(audit.IncompleteRunError):
                    audit.Auditor(root, queue, source).audit()

    def test_tampering_is_detected_without_repairing_evidence(self):
        with self.temporary() as temp:
            root, queue, source = self.fixture(Path(temp))
            task = root / "runs/gpt6astrap30/tasks/issue_000"
            cases = []
            cases.append((task / "workspace/buggy.py", b"human modification", "workspace_candidate_hash_changed"))
            manifest = root / "runs/gpt6solp30/manifest.json"
            changed = audit.read_json(manifest)
            changed["tasks"][0]["version"] = "9.9.9"
            cases.append((manifest, json.dumps(changed).encode(), "selection_differs_from_claude_30"))
            traj = audit.read_json(task / "traj.json")
            traj["messages"][1]["content"] += "\nHidden test intent injected"
            cases.append((task / "traj.json", json.dumps(traj).encode(), "rendered_initial_prompt_changed_or_extra_input"))
            cases.append((root / "records/gpt_p30_sources/openai_model.py", b"modified model", "frozen_source_hash_changed"))
            cases.append((root / "records/gpt_p30_harness_preflight/synthetic/1.2.3/command_audit/stdout.txt", b"shell startup denied", "harness_preflight_evidence_mismatch"))
            result = audit.read_json(task / "result.json")
            result["baseline_valid"] = False
            cases.append((task / "result.json", json.dumps(result).encode(), "final_baseline_not_valid"))
            for path, altered, expected in cases:
                original, stamp = path.read_bytes(), path.stat().st_mtime_ns
                with self.subTest(expected=expected):
                    path.write_bytes(altered)
                    report = audit.Auditor(root, queue, source).audit()
                    self.assertFalse(report["passed"])
                    self.assertIn(expected, {item["code"] for item in report["findings"]})
                    self.assertEqual(path.read_bytes(), altered)
                path.write_bytes(original)
                os.utime(path, ns=(stamp, stamp))

    def test_global_barrier_detects_test_during_another_generation(self):
        with self.temporary() as temp:
            root, queue, source = self.fixture(Path(temp))
            early = root / "runs/gpt6astrap30/tasks/issue_000/logs/original.stdout.txt"
            own_end = (early.parents[1] / "agent_result.json").stat().st_mtime
            os.utime(early, (own_end + 4, own_end + 4))
            late = root / "runs/gpt6solp30/tasks/issue_029/traj.json"
            os.utime(late, (own_end + 10, own_end + 10))
            report = audit.Auditor(root, queue, source).audit()
            codes = {item["code"] for item in report["findings"]}
            self.assertIn("global_final_tests_preceded_completion_of_all_90_agents", codes)
            self.assertIn("generation_barrier_chronology_invalid", codes)

    def test_orphan_response_and_missing_claim_are_detected(self):
        with self.temporary() as temp:
            root, queue, source = self.fixture(Path(temp))
            next(queue.glob("*.claimed.json")).unlink()
            write(queue / ("a" * 32 + ".response.json"), native_response("gpt-6-sol", "orphan", time.time()))
            report = audit.Auditor(root, queue, source).audit()
            codes = {item["code"] for item in report["findings"]}
            self.assertIn("broker_claim_missing", codes)
            self.assertIn("orphan_broker_response_artifacts", codes)

    def test_deleted_and_empty_candidates_preserve_exact_bytes_and_failure(self):
        with self.temporary() as temp:
            root, queue, source = self.fixture(Path(temp))
            task = root / "runs/gpt6astrap30/tasks/issue_000"
            candidate = task / "workspace/buggy.py"
            for deleted in (False, True):
                with self.subTest(deleted=deleted):
                    if deleted:
                        candidate.unlink()
                    else:
                        candidate.write_bytes(b"")
                    (task / "patched.py").write_bytes(b"")
                    path = task / "agent_result.json"
                    stamp = path.stat().st_mtime
                    agent = audit.read_json(path) | {"candidate_present": not deleted, "candidate_sha256": audit.EMPTY_SHA256}
                    write(path, agent, stamp)
                    result = audit.read_json(task / "result.json")
                    result.update(candidate_missing=deleted, repaired=False)
                    result["candidate"].update(source_sha256=audit.EMPTY_SHA256, status="ERROR")
                    write(task / "result.json", result)
                    write(task / "logs/candidate.json", result["candidate"])
                    barrier_path = root / "records/gpt_p30_generation_barrier.json"
                    barrier = audit.read_json(barrier_path)
                    entry = next(item for item in barrier["cases"] if item["folder"] == "gpt6astrap30" and item["case"] == "issue_000")
                    entry.update(agent_result_sha256=digest(path), candidate_sha256=audit.EMPTY_SHA256)
                    write(barrier_path, barrier)
                    report = audit.Auditor(root, queue, source).audit()
                    self.assertTrue(report["passed"], report["findings"])
                    self.assertEqual(report["runs"]["gpt6astrap30"]["repaired"], 29)
                    self.assertEqual(candidate.exists(), not deleted)
                    self.assertEqual((task / "patched.py").read_bytes(), b"")

    def test_write_only_creates_new_gpt_reports(self):
        with self.temporary() as temp:
            root, queue, source = self.fixture(Path(temp))
            before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
            args = ["audit_gpt_runs.py", "--root", str(root), "--queue", str(queue), "--default-agent-source", str(source), "--write"]
            with patch("sys.argv", args), patch("sys.stdout", io.StringIO()):
                self.assertEqual(audit.main(), 0)
            after = {path for path in root.rglob("*") if path.is_file()}
            expected = {root / "records/gpt_p30_final_audit.json"} | {root / "runs" / folder / "final_audit.json" for folder in audit.MODELS}
            self.assertEqual(after - set(before), expected)
            self.assertTrue(all(path.read_bytes() == value for path, value in before.items()))

    def test_usage_counts_cached_input_and_reasoning_only_once(self):
        prices = {"input_per_million": 2, "output_per_million": 10, "cache_read_per_million": .2, "cache_write_per_million": 2.5}
        usage = {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120, "input_tokens_details": {"cached_tokens": 25, "cache_write_tokens": 5}, "output_tokens_details": {"reasoning_tokens": 15}}
        self.assertAlmostEqual(audit.usage_cost(prices, usage), .0003575)
        large = usage | {"input_tokens": 272001, "total_tokens": 272021}
        expected = ((272001 - 30) * 2 + 25 * .2 + 5 * 2.5) * 2 + 20 * 10 * 1.5
        self.assertAlmostEqual(audit.usage_cost(prices, large), expected / 1_000_000)
        for malformed in (usage | {"input_tokens": True}, usage | {"total_tokens": 121}, usage | {"input_tokens_details": {"cached_tokens": 101}}, usage | {"output_tokens_details": {"reasoning_tokens": 21}}):
            with self.assertRaises(ValueError):
                audit.usage_cost(prices, malformed)
        with self.assertRaises(ValueError):
            audit.usage_cost({"input_per_million": 2, "output_per_million": 10}, usage)

    def test_incomplete_and_format_error_responses_remain_billed(self):
        model, stamp = "gpt-6-sol", time.time()
        messages = []
        for index, status in enumerate(("completed", "incomplete")):
            response = native_response(model, "resp" + str(index), stamp)
            response.update(status=status, output=[{"type": "message", "content": [{"type": "output_text", "text": "missing bash"}]}])
            cost = audit.usage_cost(audit.PRICES[model], response["usage"])
            messages.append({"role": "assistant", "content": response["output"], "extra": {"response": response, "usage": response["usage"], "cost": cost, "cost_status": "priced", "timestamp": stamp}})
            messages.append({"role": "user", "content": "format correction", "extra": {"interrupt_type": "FormatError"}})
        tally = audit.trajectory_usage({"messages": messages}, model, audit.PRICES[model])
        self.assertEqual(tally["problems"], [])
        self.assertEqual(tally["native_responses"], 2)
        self.assertEqual(tally["billed_turns_without_executable_action"], 2)
        self.assertAlmostEqual(tally["cost_usd"], 2 * .000264)
        messages[0]["extra"]["cost_status"] = "unknown"
        self.assertTrue(audit.trajectory_usage({"messages": messages}, model, audit.PRICES[model])["problems"])

    def test_http_400_terminal_attempt_reconciles_without_inventing_native_usage(self):
        model, folder, stamp = "gpt-6-sol", "gpt6solp30", time.time()
        response = native_response(model, "before_400", stamp)
        cost = audit.usage_cost(audit.PRICES[model], response["usage"])
        messages = [{"role": "system", "content": "Synthetic system"}, {"role": "user", "content": "Synthetic task"}]
        assistant = {"role": "assistant", "content": response["output"], "extra": {"response": response, "usage": response["usage"], "cost": cost, "cost_status": "priced", "timestamp": stamp,
                     "actions": [{"command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT", "tool_call_id": response["output"][0]["call_id"]}]}}
        common = {"model": model, "tools": [audit.BASH_TOOL], "tool_choice": "auto", "parallel_tool_calls": False, "max_output_tokens": 8192, "store": False, "include": ["reasoning.encrypted_content"]}
        request1 = common | {"input": audit.history_input(messages)}
        messages.extend([assistant, {"role": "user", "content": [{"type": "function_call_output", "call_id": response["output"][0]["call_id"], "output": "Synthetic observation"}]}])
        request2 = common | {"input": audit.history_input(messages)}
        messages.append({"role": "exit", "content": "HTTP 400", "extra": {"exit_status": "RuntimeError"}})
        trajectory = {"messages": messages, "info": {"model_stats": {"api_calls": 2, "instance_cost": cost}}}
        with self.temporary() as temp:
            auditor = audit.Auditor(Path(temp))
            auditor.prices = audit.PRICES
            native = {"request_id": "native", "request": request1, "response": response, "request_mtime": stamp - 1, "response_mtime": stamp}
            rejected = {"request_id": "rejected", "request": request2, "response": {"http_status": 400, "error": {"type": "invalid_request_error", "message": "Synthetic API rejection"}}, "request_mtime": stamp + 1, "response_mtime": stamp + 2}
            auditor.response_map = {response["id"]: native}
            auditor.queue_records = {"native": native, "rejected": rejected}
            tally = auditor.reconcile_trajectory(folder, "issue_000", trajectory, {"steps": 2, "cost_usd": cost}, {"accepted_response_models": [model]})
            self.assertEqual(auditor.findings, [])
            self.assertEqual(tally["native_responses"], 1)
            self.assertEqual(tally["cost_usd"], cost)
            self.assertEqual(auditor.claimed_requests, {"native", "rejected"})

    def test_broker_rejection_is_distinct_from_ambiguous_transport_usage(self):
        with self.temporary() as temp:
            root = Path(temp)
            queue = audit.default_queue_path(root)
            write(queue / "startup.json", {"preflight_ok": True, "allowed_models": list(audit.MODELS.values())})
            request_id, stamp = "1" * 32, time.time()
            write(queue / (request_id + ".request.json"), {"model": "gpt-6-sol"}, stamp)
            write(queue / (request_id + ".claimed.json"), {"claimed": True, "model": "gpt-6-sol", "claimed_at": iso(stamp)})
            for status in (400, 429, 500, None):
                with self.subTest(status=status):
                    write(queue / (request_id + ".response.json"), {"error": {"type": "synthetic_error"}, "http_status": status})
                    auditor = audit.Auditor(root)
                    auditor.load_queue()
                    codes = {finding["code"] for finding in auditor.findings}
                    self.assertIn("broker_error_response", codes)
                    self.assertEqual("broker_transport_error_has_uncertain_billed_usage" in codes, status in (500, None))

    def test_model_aliases_require_explicit_dated_allowlist(self):
        model = "gpt-6-sol"
        self.assertEqual(audit.accepted_models(model, {}), {model})
        self.assertEqual(audit.accepted_models(model, {"accepted_response_models": [model + "-2026-10-08"]}), {model, model + "-2026-10-08"})
        for name in ("gpt-6-astra", model + "-preview", model + "-latest", model + "-anything"):
            with self.assertRaises(ValueError):
                audit.accepted_models(model, {"accepted_response_models": [name]})


if __name__ == "__main__":
    unittest.main()
