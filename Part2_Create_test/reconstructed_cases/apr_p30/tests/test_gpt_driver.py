"""Offline GPT orchestration checks with synthetic files and inert agents."""
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch


def load_driver():
    source = Path(__file__).resolve().parents[1] / "tools/gpt_p30.py"
    spec = importlib.util.spec_from_file_location("gpt_driver_contract_module", source)
    module = importlib.util.module_from_spec(spec)
    # Restore the test process environment after the runner's credential scrub.
    with patch.dict(os.environ):
        spec.loader.exec_module(module)
    return module


driver = load_driver()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def config():
    return {
        "agent": {"system_template": "repair", "instance_template": "/work/buggy.py {{title}}",
                  "step_limit": 40, "cost_limit": 1.0, "wall_time_limit_seconds": 1200},
        "model": {"observation_template": "observation", "format_error_template": "format error"},
    }


class GPTDriverTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.root_patch = patch.object(driver, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def task_files(self, index=0, spec=None, *, closed=False, candidate=b"print('candidate')\n"):
        spec = spec or driver.SPECS[0]
        case = f"synthetic_{index:03}"
        source = self.root / "synthetic_sources" / case
        source.mkdir(parents=True, exist_ok=True)
        data = {"buggy.py": b"print('original')\n", "fixed.py": b"print('reference')\n", "test.py": b"# inert synthetic test\n"}
        for name, raw in data.items():
            (source / name).write_bytes(raw)
        task = {"case": case, "row": index, "version": "1.2.3", "interpreter": "synthetic-python",
                "source_dir": str(source), "support_path": None, "hashes": {name: digest(raw) for name, raw in data.items()}}
        target = self.root / "runs" / spec["folder"] / "tasks" / case
        (target / "workspace").mkdir(parents=True, exist_ok=True)
        (target / "validator").mkdir(exist_ok=True)
        (target / "original.py").write_bytes(data["buggy.py"])
        (target / "validator/test.py").write_bytes(data["test.py"])
        (target / "workspace/buggy.py").write_bytes(data["buggy.py"] if not closed else candidate)
        write_json(target / "agent_input.json", {"title": "Synthetic title", "question": "Synthetic question"})
        if closed:
            (target / "patched.py").write_bytes(candidate)
            write_json(target / "traj.json", {"messages": [{"role": "exit", "content": "Submitted"}]})
            write_json(target / "agent_result.json", {
                "case": case, "version": task["version"], "model": spec["model"],
                "candidate_sha256": digest(candidate), "candidate_present": True,
                "finished_at": "2026-01-01T00:00:00+00:00", "submitted": True,
            })
        return task, target

    def closed_manifests(self):
        manifests = []
        for spec in driver.SPECS:
            tasks = [self.task_files(index, spec, closed=True)[0] for index in range(30)]
            manifests.append({"count": 30, "tasks": tasks})
        return manifests

    def test_case_identity_version_interpreter_and_hashes_are_frozen(self):
        tasks = [{"case": f"synthetic_{i}", "version": "1.2.3", "interpreter": "python",
                  "hashes": {"buggy.py": str(i), "test.py": "test"}} for i in range(30)]
        baseline = {"count": 30, "tasks": tasks}
        driver.assert_comparable([baseline, deepcopy(baseline)])
        for field in ("case", "version", "interpreter", "hashes"):
            altered = deepcopy(baseline)
            altered["tasks"][0][field] = {"buggy.py": "changed"} if field == "hashes" else "changed"
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "differ"):
                driver.assert_comparable([baseline, altered])
        duplicate = deepcopy(baseline)
        duplicate["tasks"][-1] = deepcopy(duplicate["tasks"][0])
        with self.assertRaisesRegex(ValueError, "unique"):
            driver.assert_comparable([duplicate])

    def test_source_freeze_is_idempotent_and_refuses_changed_source(self):
        libraries = self.root / "synthetic_libraries"
        default = libraries / "minisweagent/agents/default.py"
        default.parent.mkdir(parents=True)
        default.write_bytes(b"# synthetic DefaultAgent\n")
        original_config = self.root / "upstream/configs/apr.yaml"
        original_config.parent.mkdir(parents=True)
        original_config.write_bytes(b"synthetic: true\n")
        (self.root / "tools").mkdir()
        for name in ("one.py", "two.py"):
            (self.root / "tools" / name).write_bytes(name.encode())
        with patch.object(driver, "LIBRARIES", libraries), patch.object(driver, "SOURCE_NAMES", ("one.py", "two.py")):
            first = driver.freeze_sources()
            self.assertEqual(driver.freeze_sources(), first)
            (self.root / "tools/one.py").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "Frozen experiment source changed"):
                driver.freeze_sources()
        self.assertEqual((self.root / "records/gpt_p30_sources/one.py").read_bytes(), b"one.py")

    def test_missing_candidate_hash_is_empty_but_presence_is_distinguished(self):
        task, target = self.task_files(closed=True, candidate=b"")
        empty_hash = driver.candidate_hash(target / "workspace/buggy.py")
        (target / "workspace/buggy.py").unlink()
        self.assertEqual(driver.candidate_hash(target / "workspace/buggy.py"), empty_hash)
        with self.assertRaisesRegex(ValueError, "Candidate changed"):
            driver.verify_closed(driver.SPECS[0], task)
        row = driver.adapter.read_json(target / "agent_result.json")
        row["candidate_present"] = False
        write_json(target / "agent_result.json", row)
        self.assertFalse(driver.verify_closed(driver.SPECS[0], task)["candidate_present"])

    def test_closed_run_rejects_candidate_snapshot_trajectory_and_input_tampering(self):
        tampering = [
            ("workspace/buggy.py", b"changed", "Candidate changed"),
            ("patched.py", b"changed", "snapshot changed"),
            ("traj.json", b'{"messages":[{"role":"user"}]}', "not closed"),
            ("validator/test.py", b"changed", "validator test changed"),
            ("original.py", b"changed", "repair snapshot changed"),
        ]
        for index, (name, raw, expected) in enumerate(tampering):
            task, target = self.task_files(index, closed=True)
            (target / name).write_bytes(raw)
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, expected):
                driver.verify_closed(driver.SPECS[0], task)
        task, target = self.task_files(20, closed=True)
        row = driver.adapter.read_json(target / "agent_result.json")
        row["model"] = "other-model"
        write_json(target / "agent_result.json", row)
        with self.assertRaisesRegex(ValueError, "identity"):
            driver.verify_closed(driver.SPECS[0], task)

    def test_generation_barrier_requires_all_closed_runs_and_is_immutable(self):
        manifests = self.closed_manifests()
        final = self.root / "runs" / driver.SPECS[-1]["folder"] / "tasks/synthetic_029/agent_result.json"
        saved = final.read_bytes()
        final.unlink()
        receipt = self.root / "records/gpt_p30_generation_barrier.json"
        with self.assertRaises(FileNotFoundError):
            driver.generation_barrier(manifests)
        self.assertFalse(receipt.exists())
        final.write_bytes(saved)
        first = driver.generation_barrier(manifests)
        self.assertEqual(first["total_cases"], 90)
        self.assertEqual(len({(row["folder"], row["case"]) for row in first["cases"]}), 90)
        initial_receipt_bytes = receipt.read_bytes()
        self.assertEqual(driver.generation_barrier(manifests), first)
        self.assertEqual(receipt.read_bytes(), initial_receipt_bytes)
        changed = json.loads(saved)
        changed["finished_at"] = "2026-01-02T00:00:00+00:00"
        write_json(final, changed)
        with self.assertRaisesRegex(ValueError, "changed after validation barrier"):
            driver.generation_barrier(manifests)
        self.assertEqual(receipt.read_bytes(), initial_receipt_bytes)

    def test_generation_barrier_rejects_duplicate_or_wrong_number_of_manifests(self):
        manifests = self.closed_manifests()
        duplicate = deepcopy(manifests)
        for manifest in duplicate:
            manifest["tasks"][-1] = deepcopy(manifest["tasks"][0])
        for invalid in (duplicate, manifests + [deepcopy(manifests[0])], manifests[:2]):
            with self.subTest(count=len(invalid)), self.assertRaises(ValueError):
                driver.generation_barrier(invalid)
        self.assertFalse((self.root / "records/gpt_p30_generation_barrier.json").exists())

    def test_file_transport_preserves_rejected_native_response_for_usage_accounting(self):
        queue = self.root / "queue"
        queue.mkdir()
        native = {"object": "response", "model": "wrong-model", "output": [],
                  "usage": {"input_tokens": 100, "output_tokens": 10}}
        request_id = "a" * 32
        write_json(queue / (request_id + ".response.json"), {
            "error": {"type": "model_mismatch", "message": "rejected"}, "native_response": native,
        })
        with patch.object(driver.uuid, "uuid4", return_value=Mock(hex=request_id)):
            result = driver.FileTransport(queue)({"model": "requested", "input": "synthetic"})
        self.assertEqual(result, native)
        self.assertEqual(driver.adapter.read_json(queue / (request_id + ".request.json"))["input"], "synthetic")

    def test_file_transport_timeout_persists_one_request_without_replay(self):
        queue = self.root / "queue"
        queue.mkdir()
        with patch.object(driver.time, "monotonic", side_effect=[0, 211]):
            with self.assertRaisesRegex(TimeoutError, "will not be replayed"):
                driver.FileTransport(queue)({"model": "requested"})
        self.assertEqual(len(list(queue.glob("*.request.json"))), 1)

    def test_file_transport_returns_paid_native_failed_response_unchanged(self):
        queue = self.root / "queue"
        queue.mkdir()
        native = {"object": "response", "model": "requested", "status": "failed", "output": [],
                  "error": {"code": "server_error", "message": "failed"},
                  "usage": {"input_tokens": 100, "output_tokens": 10}}
        request_id = "b" * 32
        write_json(queue / (request_id + ".response.json"), native)
        with patch.object(driver.uuid, "uuid4", return_value=Mock(hex=request_id)):
            self.assertEqual(driver.FileTransport(queue)({"model": "requested", "input": "synthetic"}), native)

    def test_run_one_finalizes_deleted_candidate_and_cannot_rerun_it(self):
        task, target = self.task_files()
        spec = driver.SPECS[0]
        queue = self.root / "queue"
        write_json(queue / "ready.json", {"accepted_response_models": {spec["model"]: [spec["model"]]}})
        write_json(target.parents[1] / "manifest.json", {"accepted_response_models": [spec["model"]]})
        env = Mock()
        env.execute.return_value = {"returncode": 1, "output": "synthetic native error"}
        agent = Mock(n_calls=40, cost=0.25)

        def delete_and_finish(**kwargs):
            (target / "workspace/buggy.py").unlink()
            write_json(target / "traj.json", {"messages": [
                {"role": "assistant", "content": [], "extra": {"response": {"usage": {}}, "cost_status": "priced"}},
                {"role": "exit", "content": "LimitsExceeded"},
            ]})
            return {"exit_status": "LimitsExceeded"}

        agent.run.side_effect = delete_and_finish
        with (patch.object(driver, "MonitoredBashEnvironment", return_value=env) as environment,
             patch.object(driver, "OpenAIResponsesModel") as model,
             patch.object(driver, "DefaultAgent", return_value=agent) as make_agent,
             patch("builtins.print")):
            row = driver.run_one(spec, task, config(), queue)
            self.assertEqual(driver.run_one(spec, task, config(), queue), row)
        self.assertFalse(row["candidate_present"])
        self.assertFalse(row["submitted"])
        self.assertEqual(row["candidate_sha256"], digest(b""))
        self.assertEqual((target / "patched.py").read_bytes(), b"")
        self.assertEqual(row["cost_statuses"], ["priced"])
        self.assertFalse(row["candidate_test_feedback"])
        self.assertFalse((target / "result.json").exists())
        environment.assert_called_once()
        make_agent.assert_called_once()
        env.execute.assert_called_once_with({"command": "$PY buggy.py"})
        self.assertEqual(model.call_args.kwargs["max_tokens"], 8192)
        self.assertEqual(make_agent.call_args.kwargs["step_limit"], 40)
        self.assertEqual(make_agent.call_args.kwargs["cost_limit"], 1)
        self.assertEqual(agent.run.call_args.kwargs["question"], "Synthetic question")

    def test_run_one_refuses_unresolved_trajectory_or_modified_starting_code(self):
        for index, changed in enumerate(("trajectory", "candidate")):
            task, target = self.task_files(index)
            if changed == "trajectory":
                write_json(target / "traj.json", {"messages": []})
            else:
                (target / "workspace/buggy.py").write_bytes(b"changed before agent")
            with patch.object(driver, "DefaultAgent") as agent, patch.object(driver, "MonitoredBashEnvironment") as env:
                with self.subTest(changed=changed), self.assertRaises(ValueError):
                    driver.run_one(driver.SPECS[0], task, config(), self.root / "queue")
            agent.assert_not_called()
            env.assert_not_called()

    def test_harness_preflight_checks_each_pinned_interpreter_and_records_success(self):
        tasks = [{"version": version, "interpreter": f"synthetic-python-{version}",
                  "support_path": "/synthetic/py312" if version == "2.5.0" else None}
                 for version in ("2.5.0", "0.46.3", "0.25.3", "2.5.0")]
        environment = Mock()
        environment.execute.return_value = {"returncode": 0, "output": "731942\r\n"}
        with (patch.object(driver, "MonitoredBashEnvironment", return_value=environment) as constructor,
              patch.object(driver, "OpenAIResponsesModel") as model, patch.object(driver, "FileTransport") as transport,
              patch("builtins.print")):
            driver.harness_preflight([{"tasks": tasks}])
        self.assertEqual(constructor.call_count, 3)
        self.assertEqual(environment.execute.call_count, 3)
        self.assertEqual({call.args[1] for call in constructor.call_args_list},
                         {task["interpreter"] for task in tasks})
        for call in environment.execute.call_args_list:
            self.assertEqual(call.args[0], {"command": '$PY -c "print(731942)"'})
        support_call = next(call for call in constructor.call_args_list if call.args[1].endswith("2.5.0"))
        self.assertEqual(support_call.kwargs["support_path"], str(self.root / "support/py312"))
        receipts = list((self.root / "records/gpt_p30_harness_preflight").glob("*/receipt.json"))
        self.assertEqual(len(receipts), 1)
        receipt = driver.adapter.read_json(receipts[0])
        self.assertEqual(len(receipt["checks"]), 3)
        self.assertTrue(all(check["passed"] for check in receipt["checks"]))
        self.assertTrue(receipt["checked_at"])
        model.assert_not_called()
        transport.assert_not_called()

    def test_harness_preflight_stops_and_records_failure_before_api_calls(self):
        tasks = [{"version": version, "interpreter": "synthetic-python", "support_path": None}
                 for version in ("0.25.3", "0.46.3", "2.5.0")]
        for index, result in enumerate((
            {"returncode": 1, "output": "NtCreateDirectoryObject denied"},
            {"returncode": 0, "output": "unexpected output"},
            {"returncode": 1, "output": "731942"},
        )):
            request_id = f"{index:032x}"
            environment = Mock()
            environment.execute.return_value = result
            with (self.subTest(result=result), patch.object(driver.uuid, "uuid4", return_value=Mock(hex=request_id)),
                  patch.object(driver, "MonitoredBashEnvironment", return_value=environment) as constructor,
                  patch.object(driver, "OpenAIResponsesModel") as model, patch.object(driver, "FileTransport") as transport):
                with self.assertRaisesRegex(RuntimeError, "preflight failed before API calls"):
                    driver.harness_preflight([{"tasks": tasks}])
            constructor.assert_called_once()
            environment.execute.assert_called_once()
            model.assert_not_called()
            transport.assert_not_called()
            receipt = driver.adapter.read_json(self.root / "records/gpt_p30_harness_preflight" / request_id / "receipt.json")
            self.assertEqual(receipt["checks"], [{"version": "0.25.3", "returncode": result["returncode"], "passed": False}])


if __name__ == "__main__":
    unittest.main()
