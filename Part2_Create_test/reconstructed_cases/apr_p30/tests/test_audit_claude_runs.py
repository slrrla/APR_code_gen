"""Offline auditor tests. All sources, validators and API artifacts are synthetic."""
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
import zipfile

import audit_claude_runs as audit


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive_queue(queue):
    archive = queue.parent / "records/api_queue.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    index = {"schema_version": 1, "original_directory": "api_queue", "files": {}}
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        for path in sorted(queue.rglob("*")):
            if not path.is_file():
                continue
            name = path.relative_to(queue).as_posix()
            content = path.read_bytes()
            index["files"][name] = {"sha256": hashlib.sha256(content).hexdigest(),
                                    "bytes": len(content), "mtime_ns": path.stat().st_mtime_ns}
            zipped.writestr(name, content)
        zipped.writestr("_archive_index.json", json.dumps(index))
    return archive


def native_response(model, identifier):
    return {"id": identifier, "type": "message", "role": "assistant", "model": model,
            "content": [{"type": "tool_use", "id": "tool" + identifier, "name": "bash",
                         "input": {"command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"}}],
            "usage": {"input_tokens": 100, "output_tokens": 10}, "stop_reason": "tool_use"}


class AuditContracts(unittest.TestCase):
    def fixture(self, base):
        root = base / "cases/apr_p30"
        root.mkdir(parents=True)
        queue = root / "api_queue"
        queue.mkdir()
        for filename in audit.HARNESSES:
            (root / filename).write_text("synthetic harness bytes", encoding="utf-8")
        default_source = root / "default_agent.py"
        default_source.write_text("synthetic native agent bytes", encoding="utf-8")
        interpreter = root / "python.exe"
        interpreter.write_bytes(b"synthetic interpreter bytes, never executed")
        config = root / "upstream/configs/apr.yaml"
        config.parent.mkdir(parents=True)
        config.write_text("synthetic configuration", encoding="utf-8")
        stamp = time.time()
        selected = []
        for index in range(30):
            case = f"issue_{index:03}"
            source = root.parent / case
            source.mkdir()
            for filename in audit.SOURCES:
                (source / filename).write_text("synthetic " + filename, encoding="utf-8")
            selected.append({"case": case, "version": "1.2.3", "interpreter": str(interpreter),
                             "source_dir": str(source), "hashes": {name: digest(source / name) for name in audit.SOURCES}})
        write(root / "runs/codex_p30/manifest.json", {"count": 30, "tasks": selected})
        write(queue / "ready.json", {"broker_source_sha256": digest(root / "claude_api_broker.py")})
        for folder, model in audit.MODELS.items():
            run = root / "runs" / folder
            write(run / "manifest.json", {"count": 30, "tasks": selected, "actual_model": model,
                                          "candidate_test_feedback": False, "mcp_used": False,
                                          "runner_sources": {name: digest(root / name) for name in audit.HARNESSES},
                                          "default_agent_source_sha256": digest(default_source)})
            write(run / "experiment.json", {"status": "complete", "original_config_sha256": digest(config)})
            write(run / "environment_probes/1.2.3/probe.json", {"qiskit": "1.2.3", "interpreter": str(interpreter), "interpreter_sha256": digest(interpreter)})
            for index, task in enumerate(selected):
                tdir = run / "tasks" / task["case"]
                write(tdir / "agent_input.json", {"case": task["case"], "version": task["version"], "title": "Synthetic " + task["case"], "question": "Synthetic question"})
                (tdir / "original.py").write_bytes((Path(task["source_dir"]) / "buggy.py").read_bytes())
                validator = tdir / "validator/test.py"
                validator.parent.mkdir()
                validator.write_bytes((Path(task["source_dir"]) / "test.py").read_bytes())
                candidate = tdir / "workspace/buggy.py"
                candidate.parent.mkdir()
                candidate.write_text("synthetic generated repair", encoding="utf-8")
                (tdir / "patched.py").write_bytes(candidate.read_bytes())
                response = native_response(model, "msg_" + folder + task["case"])
                cost = audit.usage_cost(model, response["usage"])
                first = "Synthetic " + task["case"] + "\nSynthetic question"
                command = {"id": 1, "session_id": "synthetic-session", "command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT",
                           "time_utc": datetime.fromtimestamp(stamp, timezone.utc).isoformat(), "status": "SUBMITTED", "seconds": .01}
                trajectory = {"info": {"exit_status": "Submitted", "model_stats": {"instance_cost": cost, "api_calls": 1},
                                        "config": {"agent_type": "minisweagent.agents.default.DefaultAgent", "model": {"model_name": model},
                                                   "agent": {"step_limit": 40, "cost_limit": 1, "wall_time_limit_seconds": 1200}}},
                              "messages": [{"role": "user", "content": first},
                                           {"role": "assistant", "content": response["content"],
                                            "extra": {"response": response, "usage": response["usage"], "cost": cost,
                                                      "timestamp": stamp, "actions": [{"command": command["command"]}]}},
                                           {"role": "exit", "content": "", "extra": {"exit_status": "Submitted"}}],
                              "environment_commands": [command]}
                write(tdir / "traj.json", trajectory)
                write(tdir / "agent_result.json", {"case": task["case"], "version": task["version"], "model": model, "exit_status": "Submitted",
                                                   "submitted": True, "steps": 1, "cost_usd": cost, "candidate_test_feedback": False, "candidate_sha256": digest(candidate)})
                os.utime(tdir / "agent_result.json", (stamp + 1, stamp + 1))
                command_path = tdir / "command_audit/commands.jsonl"
                command_path.parent.mkdir()
                command_path.write_text(json.dumps({"event": "attempt", **{key: value for key, value in command.items() if key not in {"status", "seconds"}}}) + "\n"
                                        + json.dumps({"event": "result", **command}) + "\n", encoding="utf-8")
                result = {"candidate": {"status": "PASS"}, "original": {"status": "FAIL"}, "reference": {"status": "PASS"}, "repaired": True}
                for variant, source_hash in (("original", task["hashes"]["buggy.py"]), ("reference", task["hashes"]["fixed.py"]), ("candidate", digest(candidate))):
                    result[variant].update(source_sha256=source_hash, test_sha256=task["hashes"]["test.py"])
                    write(tdir / "logs" / (variant + ".json"), {"seconds": .1})
                    output = tdir / "logs" / (variant + ".stdout.txt")
                    output.write_text("synthetic output", encoding="utf-8")
                    os.utime(output, (stamp + 5, stamp + 5))
                write(tdir / "result.json", result)
                request_id = hashlib.md5((folder + task["case"]).encode()).hexdigest()
                request_path, response_path = queue / (request_id + ".request.json"), queue / (request_id + ".response.json")
                write(request_path, {"model": model, "messages": [{"role": "user", "content": first}]})
                write(response_path, response)
                os.utime(request_path, (stamp - 1, stamp - 1))
                os.utime(response_path, (stamp, stamp))
            unit_cost = audit.usage_cost(model, {"input_tokens": 100, "output_tokens": 10})
            write(run / "experiment_result.json", {"cost_usd": round(30 * unit_cost, 6), "pipeline_smoke_cost_usd": 0})
        return root, queue, default_source

    def test_complete_same_30_synthetic_runs_pass_and_reconcile_costs(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            report = audit.Auditor(root, queue, default_source).audit()
            self.assertTrue(report["passed"], report["findings"])
            self.assertEqual(report["broker_native_responses"], 60)
            self.assertEqual(report["runs"]["sonnet5.5p30"]["official_cost_usd"], .009)
            self.assertEqual(report["runs"]["haiku5p30"]["official_cost_usd"], .0045)
            self.assertEqual(report["credential_pattern_findings"], [])

    def test_archived_queue_preserves_audit_results_after_directory_is_moved(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            original = audit.Auditor(root, queue, default_source).audit()
            archive = archive_queue(queue)
            queue.rename(root / "unpacked_queue")
            self.assertEqual(audit.default_queue_path(root), archive)
            archived = audit.Auditor(root, archive, default_source).audit()
            self.assertTrue(archived["passed"], archived["findings"])
            for key in ("runs", "broker_native_responses", "broker_request_count", "broker_usage_cost_usd_by_model"):
                self.assertEqual(archived[key], original[key])

    def test_archived_queue_retains_integer_nanosecond_chronology(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            request = next(queue.glob("*.request.json"))
            response = request.with_name(request.name.replace(".request.json", ".response.json"))
            os.utime(request, ns=(1_700_000_000_123_456_700, 1_700_000_000_123_456_700))
            os.utime(response, ns=(1_700_000_001_987_654_300, 1_700_000_001_987_654_300))
            expected = request.stat().st_mtime_ns, response.stat().st_mtime_ns
            archive = archive_queue(queue)
            auditor = audit.Auditor(root, archive, default_source)
            auditor.load_queue()
            record = auditor.queue_records[request.name.removesuffix(".request.json")]
            self.assertEqual((record["request_mtime_ns"], record["response_mtime_ns"]), expected)
            self.assertEqual(record["request_mtime"], expected[0] / 1_000_000_000)
            self.assertEqual(record["response_mtime"], expected[1] / 1_000_000_000)

    def test_archived_queue_rejects_tampered_bytes_and_invalid_inventory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            queue = root / "api_queue"
            write(queue / "ready.json", {"ready": True})
            archive = archive_queue(queue)
            with zipfile.ZipFile(archive) as zipped:
                index = json.loads(zipped.read("_archive_index.json"))
            tampered = root / "tampered.zip"
            with zipfile.ZipFile(tampered, "w") as zipped:
                zipped.writestr("ready.json", json.dumps({"ready": False}))
                zipped.writestr("_archive_index.json", json.dumps(index))
            with audit.QueueArtifacts(tampered) as artifacts:
                with self.assertRaises(ValueError):
                    artifacts.json("ready.json")
            index["files"]["ready.json"].pop("mtime_ns")
            with zipfile.ZipFile(tampered, "w") as zipped:
                zipped.writestr("ready.json", (queue / "ready.json").read_bytes())
                zipped.writestr("_archive_index.json", json.dumps(index))
            with self.assertRaises(ValueError):
                with audit.QueueArtifacts(tampered):
                    pass
            index["files"] = {}
            with zipfile.ZipFile(tampered, "w") as zipped:
                zipped.writestr("ready.json", b"{}")
                zipped.writestr("_archive_index.json", json.dumps(index))
            with self.assertRaises(ValueError):
                with audit.QueueArtifacts(tampered):
                    pass

    def test_preserved_harness_snapshots_pass_without_rewriting_manifests(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            audit.capture_probe_baseline(root)
            self.assertTrue((root / "records/claude_p30_probe_baseline.json").is_file())
            snapshots = root / "records/source_snapshots/pre_cleanup"
            snapshots.mkdir(parents=True)
            tools = root / "tools"
            tools.mkdir()
            for filename in audit.HARNESSES:
                (root / filename).rename(snapshots / filename)
                (tools / filename).write_text("rewritten live harness bytes", encoding="utf-8")
            manifests = list((root / "runs").glob("*/manifest.json"))
            before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in manifests}
            report = audit.Auditor(root, queue, default_source).audit()
            self.assertTrue(report["passed"], report["findings"])
            self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in manifests})

    def test_write_uses_records_for_global_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            args = ["audit_claude_runs.py", "--root", str(root), "--queue", str(queue),
                    "--default-agent-source", str(default_source), "--write"]
            with patch("sys.argv", args), patch("sys.stdout", io.StringIO()):
                self.assertEqual(audit.main(), 0)
            self.assertTrue((root / "records/claude_p30_final_audit.json").is_file())
            self.assertFalse((root / "claude_p30_final_audit.json").exists())

    def test_incomplete_run_stops_before_reading_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            (root / "runs/haiku5p30/tasks/issue_029/result.json").unlink()
            with self.assertRaises(audit.IncompleteRunError):
                audit.Auditor(root, queue, default_source).audit()

    def test_hash_tampering_and_credential_pattern_are_reported_without_value(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            (root.parent / "issue_000/fixed.py").write_text("changed synthetic reference", encoding="utf-8")
            path = root / "runs/sonnet5.5p30/tasks/issue_000/agent_result.json"
            key = "sk-ant-" + "x" * 40
            write(path, audit.read_json(path) | {"error": key})
            report = audit.Auditor(root, queue, default_source).audit()
            self.assertFalse(report["passed"])
            codes = {finding["code"] for finding in report["findings"]}
            self.assertIn("original_source_hash_changed", codes)
            self.assertIn("credential_pattern_visible", codes)
            self.assertNotIn(key, json.dumps(report))

    def test_billed_format_error_turn_remains_in_native_usage_total(self):
        model = audit.MODELS["sonnet5.5p30"]
        response = native_response(model, "msg_format_error")
        response["content"] = [{"type": "text", "text": "missing tool"}]
        cost = audit.usage_cost(model, response["usage"])
        message = {"role": "assistant", "content": response["content"],
                   "extra": {"response": response, "usage": response["usage"], "cost": cost, "timestamp": time.time()}}
        tally = audit.trajectory_usage({"messages": [message, {"role": "user", "extra": {"interrupt_type": "FormatError"}}]}, model)
        self.assertEqual(tally["problems"], [])
        self.assertEqual(tally["billed_turns_without_executable_action"], 1)
        self.assertEqual(tally["cost_usd"], .0003)

    def test_usage_requires_explicit_valid_cache_accounting(self):
        model = audit.MODELS["haiku5p30"]
        with self.assertRaises(ValueError):
            audit.usage_cost(model, {"input_tokens": True, "output_tokens": 10})
        with self.assertRaises(ValueError):
            audit.usage_cost(model, {"input_tokens": 10, "output_tokens": 10, "cache_creation_input_tokens": 1,
                                     "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 1}})

    def test_visible_rejected_and_executed_attempts_are_distinguished(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            tdir = root / "task"
            path = tdir / "command_audit/commands.jsonl"
            path.parent.mkdir(parents=True)
            for status in ("POLICY_REJECTED", "EXECUTED"):
                record = {"id": 1, "session_id": "synthetic", "command": "cat ../fixed.py;", "status": status}
                attempt = {key: value for key, value in record.items() if key != "status"}
                path.write_text(json.dumps({"event": "attempt", **attempt}) + "\n" + json.dumps({"event": "result", **record}) + "\n", encoding="utf-8")
                auditor = audit.Auditor(root, root, root)
                report = auditor.commands({"environment_commands": [record]}, tdir, "synthetic-run", "synthetic-case")
                self.assertEqual(len(report["visible_attempts"]), 1)
                self.assertEqual(report["visible_attempts"][0]["status"], status)
                self.assertIn("withheld_reference_or_test", report["visible_attempts"][0]["categories"])
                self.assertEqual(bool(auditor.findings), status == "EXECUTED")

    def test_probe_baseline_detects_changed_interpreter_even_if_final_probe_updates(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            audit.capture_probe_baseline(root)
            interpreter = root / "python.exe"
            interpreter.write_bytes(b"changed synthetic interpreter")
            for folder in audit.MODELS:
                path = root / "runs" / folder / "environment_probes/1.2.3/probe.json"
                write(path, audit.read_json(path) | {"interpreter_sha256": digest(interpreter)})
            report = audit.Auditor(root, queue, default_source).audit()
            self.assertFalse(report["passed"])
            self.assertIn("interpreter_preparation_baseline_changed", {item["code"] for item in report["findings"]})

    def test_documented_deleted_candidate_is_a_failed_repair_without_restoration(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            tdir = root / "runs/haiku5p30/tasks/issue_000"
            (tdir / "workspace/buggy.py").unlink()
            (tdir / "patched.py").write_bytes(b"")
            agent_path = tdir / "agent_result.json"
            write(agent_path, audit.read_json(agent_path) | {"candidate_present": False, "candidate_sha256": audit.EMPTY_SHA256,
                                                            "submitted": False, "exit_status": "RuntimeError"})
            result = audit.read_json(tdir / "result.json")
            result.update(candidate_missing=True, repaired=False)
            result["candidate"].update(source_sha256=audit.EMPTY_SHA256, status="FAIL")
            write(tdir / "result.json", result)
            trajectory = audit.read_json(tdir / "traj.json")
            trajectory["info"]["exit_status"] = "RuntimeError"
            trajectory["messages"][-1]["extra"]["exit_status"] = "RuntimeError"
            trajectory["environment_commands"][0]["status"] = "EXECUTED"
            trajectory["environment_commands"][0]["command"] = "rm buggy.py"
            message = trajectory["messages"][1]
            message["content"][0]["input"]["command"] = "rm buggy.py"
            message["extra"]["response"]["content"] = deepcopy(message["content"])
            message["extra"]["actions"] = [{"command": "rm buggy.py"}]
            response_id = hashlib.md5(b"haiku5p30issue_000").hexdigest()
            write(queue / (response_id + ".response.json"), message["extra"]["response"])
            write(tdir / "traj.json", trajectory)
            command = trajectory["environment_commands"][0]
            command_path = tdir / "command_audit/commands.jsonl"
            attempt = {key: value for key, value in command.items() if key not in {"status", "seconds"}}
            command_path.write_text(json.dumps({"event": "attempt", **attempt}) + "\n" + json.dumps({"event": "result", **command}) + "\n", encoding="utf-8")
            report = audit.Auditor(root, queue, default_source).audit()
            self.assertTrue(report["passed"], report["findings"])
            row = report["runs"]["haiku5p30"]["rows"][0]
            self.assertFalse(row["candidate_present"])
            self.assertFalse(row["repaired"])
            self.assertFalse(row["submitted"])
            self.assertFalse((tdir / "workspace/buggy.py").exists())

    def test_validation_receipt_allows_only_declared_validator_functions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / "validation_audit/adapter.before.py"
            old.parent.mkdir()
            text = "VALUE = 1\ndef runtime_environment():\n    return 'unchanged'\ndef validate_task():\n    return 'old'\n"
            old.write_text(text, encoding="utf-8")
            target = root / "adapter.py"
            target.write_text(text.replace("return 'old'", "return 'new'") + "def snapshot_candidate():\n    return b''\n", encoding="utf-8")
            ended = datetime.fromtimestamp(time.time() - 10, timezone.utc).isoformat()
            applied = datetime.now(timezone.utc).isoformat()
            receipt = {"file": "adapter.py", "before_source_path": str(old), "before_sha256": digest(old), "after_sha256": digest(target),
                       "scope_functions": ["validate_task", "snapshot_candidate"], "runtime_environment_unchanged": True,
                       "applied_at_utc": applied, "agent_phase_completed_at_utc": ended, "reason": "Preserve snapshot bytes"}
            manifest = {"runner_sources": {"adapter.py": digest(old)}, "validation_adjustments": [receipt]}
            auditor = audit.Auditor(root, root, root)
            self.assertTrue(auditor.validation_adjustment(manifest, "adapter.py", "synthetic-run"))
            target.write_text(target.read_text(encoding="utf-8").replace("return 'unchanged'", "return 'changed'"), encoding="utf-8")
            receipt["after_sha256"] = digest(target)
            # New auditor clears the digest cache, matching a separate audit run.
            self.assertFalse(audit.Auditor(root, root, root).validation_adjustment(manifest, "adapter.py", "synthetic-run"))

    def test_moved_validation_receipt_checks_preserved_post_fix_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / "validation_audit/adapter.before.py"
            old.parent.mkdir()
            text = "VALUE = 1\ndef runtime_environment():\n    return 'unchanged'\ndef validate_task():\n    return 'old'\n"
            old.write_text(text, encoding="utf-8")
            target = root / "records/source_snapshots/pre_cleanup/adapter.py"
            target.parent.mkdir(parents=True)
            target.write_text(text.replace("return 'old'", "return 'new'"), encoding="utf-8")
            tools = root / "tools"
            tools.mkdir()
            (tools / "adapter.py").write_text(target.read_text().replace("VALUE = 1", "VALUE = 2"), encoding="utf-8")
            receipt = {"file": "adapter.py", "before_source_path": str(old), "before_sha256": digest(old),
                       "after_sha256": digest(target), "scope_functions": ["validate_task"], "runtime_environment_unchanged": True,
                       "applied_at_utc": datetime.now(timezone.utc).isoformat(),
                       "agent_phase_completed_at_utc": datetime.fromtimestamp(time.time() - 10, timezone.utc).isoformat()}
            manifest = {"runner_sources": {"adapter.py": digest(old)}, "validation_adjustments": [receipt]}
            moved = root / "records/validation_audit/adapter.before.py"
            moved.parent.mkdir()
            old.rename(moved)
            auditor = audit.Auditor(root, root, root)
            self.assertTrue(auditor.validation_adjustment(manifest, "adapter.py", "synthetic-run"))
            target.write_text(target.read_text().replace("VALUE = 1", "VALUE = 3"), encoding="utf-8")
            self.assertFalse(audit.Auditor(root, root, root).validation_adjustment(manifest, "adapter.py", "synthetic-run"))

    def test_late_result_finalization_does_not_reopen_a_closed_agent(self):
        with tempfile.TemporaryDirectory() as temp:
            root, queue, default_source = self.fixture(Path(temp))
            tdir = root / "runs/haiku5p30/tasks/issue_000"
            late = time.time() + 3600
            os.utime(tdir / "agent_result.json", (late, late))
            report = audit.Auditor(root, queue, default_source).audit()
            self.assertTrue(report["passed"], report["findings"])
            row = report["runs"]["haiku5p30"]["rows"][0]
            self.assertLess(row["agent_phase_end_timestamp"], row["estimated_first_test_start_timestamp"])
            trajectory = audit.read_json(tdir / "traj.json")
            trajectory["messages"].pop()
            write(tdir / "traj.json", trajectory)
            reopened = audit.Auditor(root, queue, default_source).audit()
            self.assertFalse(reopened["passed"])
            self.assertIn("trajectory_not_closed_with_exit_message", {finding["code"] for finding in reopened["findings"]})

    def test_runs_token_in_own_workspace_or_echo_is_benign_false_positive(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "runs/haiku5p30/tasks/issue_001/workspace"
            path = workspace.resolve().as_posix()
            own_workspace = "cd " + path + " && $PY buggy.py"
            echo = '$PY buggy.py > /dev/null && echo "SUCCESS: Script runs with exit code 0"'
            self.assertEqual(audit.visible_classification(own_workspace, ["prior_run_or_conversation"], workspace), "own_workspace_path_contains_runs_token")
            self.assertEqual(audit.visible_classification(echo, ["prior_run_or_conversation"], workspace), "echo_text_contains_runs_word")
            self.assertEqual(audit.visible_classification("cat ../runs/codex_p30/patch.py", ["prior_run_or_conversation"], workspace), "visible_sensitive_text")


if __name__ == "__main__":
    unittest.main()
