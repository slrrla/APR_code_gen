"""Offline broker and experiment orchestration contracts, using synthetic data only.

These tests do not open conversation records, experiment cases, fixes or validators
and cannot issue real API requests or execute generated programs.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch
import urllib.error

import claude_api_broker as broker


def load_driver():
    """Load orchestration with inert model/environment constructors."""
    model_module = types.ModuleType("claude_model")
    model_module.AnthropicMessagesModel = Mock(name="InertMessagesModel")
    model_module.TokenPrices = Mock(name="InertTokenPrices")
    environment_module = types.ModuleType("claude_environment")
    environment_module.MonitoredBashEnvironment = Mock(name="InertBashEnvironment")
    source = Path(__file__).resolve().parents[1] / "tools/claude_p30.py"
    spec = importlib.util.spec_from_file_location("claude_driver_contract_module", source)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {"claude_model": model_module, "claude_environment": environment_module}):
        spec.loader.exec_module(module)
    return module


driver = load_driver()


def config():
    return {
        "agent": {"system_template": "system", "instance_template": "/work/buggy.py {{title}}",
                  "step_limit": 40, "cost_limit": 1.0, "wall_time_limit_seconds": 1200},
        "model": {"observation_template": "observation", "format_error_template": "format error"},
    }


def tasks(count=30):
    return [
        {"case": f"issue_{index:03}", "row": index, "version": "1.2.3",
         "hashes": {"buggy.py": "buggy digest", "fixed.py": "reference digest", "test.py": "test digest"},
         "interpreter": "synthetic-python", "source_dir": "synthetic-source",
         "support_path": None, "intent": "WITHHELD DERIVED INTENT"}
        for index in range(count)
    ]


def payload(model="claude-sonnet-5-5"):
    return {"model": model, "max_tokens": 8192, "messages": [{"role": "user", "content": "synthetic task"}]}


class BrokerContracts(unittest.TestCase):
    def test_only_authorized_models_and_request_fields_reach_network(self):
        self.assertEqual(broker.MODELS, {"claude-sonnet-5-5", "claude-haiku-4-5-20251001"})
        with patch.object(broker.urllib.request, "urlopen") as network:
            self.assertEqual(broker.api_request(payload("claude-haiku-5-0"), "dummy")["error"]["type"], "unauthorized_model")
            unexpected = payload() | {"api_key": "must not be forwarded"}
            self.assertEqual(broker.api_request(unexpected, "dummy")["error"]["type"], "invalid_request")
            network.assert_not_called()

    def test_nonobject_request_is_rejected_without_network(self):
        with patch.object(broker.urllib.request, "urlopen") as network:
            result = broker.api_request([payload()], "dummy")
        self.assertEqual(result["error"]["type"], "invalid_request")
        network.assert_not_called()

    def test_response_model_must_match_the_requested_model(self):
        response = io.StringIO(json.dumps({"model": "claude-haiku-4-5-20251001", "content": []}))
        with patch.object(broker.urllib.request, "urlopen", return_value=response):
            result = broker.api_request(payload(), "dummy")
        self.assertEqual(result["error"]["type"], "model_mismatch")

    def test_http_errors_never_persist_the_credential(self):
        synthetic_key = "sk-ant-unit-test-placeholder"
        raw = json.dumps({"error": {"type": "authentication_error", "message": synthetic_key}}).encode()
        error = urllib.error.HTTPError("https://api.anthropic.com/v1/messages", 401, "Unauthorized", {}, io.BytesIO(raw))
        with patch.object(broker.urllib.request, "urlopen", side_effect=error):
            result = broker.api_request(payload(), synthetic_key)
        self.assertNotIn(synthetic_key, json.dumps(result))
        self.assertEqual(result["http_status"], 401)

    def test_ambiguous_network_failure_is_redacted_and_not_retried(self):
        synthetic_key = "sk-ant-unit-test-placeholder"
        with patch.object(broker.urllib.request, "urlopen", side_effect=TimeoutError(synthetic_key)) as network:
            result = broker.api_request(payload(), synthetic_key)
        self.assertNotIn(synthetic_key, json.dumps(result))
        self.assertEqual(network.call_count, 1)

    def test_malformed_queue_request_does_not_crash_or_block_other_requests(self):
        with tempfile.TemporaryDirectory() as temp:
            queue = Path(temp)
            bad_id, good_id = "0" * 32, "1" * 32
            (queue / (bad_id + ".request.json")).write_text("{broken JSON", encoding="utf-8")
            (queue / (good_id + ".request.json")).write_text(json.dumps(payload()), encoding="utf-8")
            (queue / "stop").touch()
            with patch.object(broker, "api_request", return_value={"model": "claude-sonnet-5-5", "content": []}) as network:
                broker.serve(queue, "dummy")
            bad = json.loads((queue / (bad_id + ".response.json")).read_text(encoding="utf-8"))
            good = json.loads((queue / (good_id + ".response.json")).read_text(encoding="utf-8"))
            self.assertIn("error", bad)
            self.assertEqual(good["model"], "claude-sonnet-5-5")
            network.assert_called_once()
            self.assertTrue((queue / "stopped.json").is_file())

    def test_broker_restart_does_not_rebill_completed_requests(self):
        with tempfile.TemporaryDirectory() as temp:
            queue = Path(temp)
            request_id = "2" * 32
            (queue / (request_id + ".request.json")).write_text(json.dumps(payload()), encoding="utf-8")
            response = {"model": "claude-sonnet-5-5", "content": [], "id": "previous-result"}
            response_path = queue / (request_id + ".response.json")
            response_path.write_text(json.dumps(response), encoding="utf-8")
            (queue / "stop").touch()
            with patch.object(broker, "api_request", return_value={"model": "claude-sonnet-5-5", "content": []}) as network:
                broker.serve(queue, "dummy")
            network.assert_not_called()
            self.assertEqual(json.loads(response_path.read_text(encoding="utf-8")), response)


class DriverContracts(unittest.TestCase):
    def test_native_agent_enforces_step_cost_and_time_budgets_before_next_query(self):
        class OfflineModel:
            def __init__(self, response_cost):
                self.calls = 0
                self.response_cost = response_cost

            def format_message(self, **kwargs):
                return kwargs

            def query(self, messages):
                self.calls += 1
                return {"role": "assistant", "content": "synthetic observation",
                        "extra": {"cost": self.response_cost, "actions": []}}

            def format_observation_messages(self, *args):
                return [{"role": "user", "content": "continue"}]

            def get_template_vars(self):
                return {}

            def serialize(self):
                return {}

        environment = Mock()
        environment.get_template_vars.return_value = {}
        environment.serialize.return_value = {}
        for response_cost, expected_calls, expected_status in [(0.01, 40, "LimitsExceeded"), (1.25, 1, "LimitsExceeded")]:
            with self.subTest(response_cost=response_cost):
                model = OfflineModel(response_cost)
                agent = driver.DefaultAgent(model, environment, **config()["agent"])
                info = agent.run(title="Synthetic title")
                self.assertEqual(info["exit_status"], expected_status)
                self.assertEqual(model.calls, expected_calls)
        model = OfflineModel(0)
        agent = driver.DefaultAgent(model, environment, **config()["agent"])
        agent._start_time -= 1201
        self.assertEqual(agent.run(title="Synthetic title")["exit_status"], "TimeExceeded")
        self.assertEqual(model.calls, 0)

    def test_preparation_exports_only_allowed_agent_input_and_requested_run_paths(self):
        selected = tasks()
        synthetic_context = {"case": "placeholder", "version": "1.2.3", "title": "Question title",
                             "question": "Sanitized question", "intent": "WITHHELD DERIVED INTENT",
                             "completion": "WITHHELD EVALUATION ADVICE", "fixed": "WITHHELD FIX"}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(driver, "ROOT", root), \
                 patch.object(driver.adapter, "prepare", side_effect=lambda *a, **k: {"count": 30, "tasks": deepcopy(selected)}), \
                 patch.object(driver.adapter, "read_json", return_value=synthetic_context), \
                 patch.object(driver.adapter, "probe_environment"), \
                 patch.object(driver.adapter, "sha", return_value="config-digest"):
                for spec in driver.SPECS:
                    manifest = driver.prepare_spec(spec, config())
                    self.assertEqual(manifest["agent_limits"], {"step_limit": 40, "cost_limit": 1.0, "wall_time_limit_seconds": 1200})
                    run = root / "runs" / spec["folder"]
                    self.assertTrue((run / "manifest.json").is_file())
                    for task in selected:
                        exported = json.loads((run / "tasks" / task["case"] / "agent_input.json").read_text(encoding="utf-8"))
                        self.assertEqual(set(exported), {"case", "version", "title", "question"})
                        self.assertNotIn("WITHHELD", json.dumps(exported))
        self.assertEqual([spec["folder"] for spec in driver.SPECS], ["sonnet5.5p30", "haiku5p30"])
        self.assertTrue(driver.SPECS[1]["replacement_authorized"])
        self.assertEqual(driver.SPECS[1]["model"], "claude-haiku-4-5-20251001")

    def _assert_invalid_selection_stops_before_repair(self, first, second):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "upstream/configs").mkdir(parents=True)
            (root / "upstream/configs/apr.yaml").write_text(json.dumps(config()), encoding="utf-8")
            queue = root / "api_queue"
            queue.mkdir()
            (queue / "ready.json").write_text(json.dumps({"ready": True, "allowed_models": sorted(broker.MODELS)}), encoding="utf-8")
            with patch.object(driver, "ROOT", root), \
                 patch.object(sys, "argv", ["claude_p30.py", "--queue", str(queue)]), \
                 patch.object(driver, "prepare_spec", side_effect=[{"count": len(first), "tasks": first}, {"count": len(second), "tasks": second}]), \
                 patch.object(driver, "run_one") as repair, \
                 patch.object(driver.adapter, "validate_all"), \
                 patch.object(driver, "save_summaries", return_value={}), \
                 self.assertRaises(ValueError):
                driver.main()
            repair.assert_not_called()

    def test_different_case_versions_cannot_be_reported_as_the_same_30(self):
        first, second = tasks(), tasks()
        second[0]["version"] = "9.9.9"
        self._assert_invalid_selection_stops_before_repair(first, second)

    def test_different_source_hashes_cannot_be_reported_as_the_same_30(self):
        first, second = tasks(), tasks()
        second[0]["hashes"]["buggy.py"] = "changed source digest"
        self._assert_invalid_selection_stops_before_repair(first, second)

    def test_incomplete_or_duplicate_selection_stops_before_repair(self):
        self._assert_invalid_selection_stops_before_repair(tasks(29), tasks(29))
        duplicate = tasks()
        duplicate[-1] = deepcopy(duplicate[0])
        self._assert_invalid_selection_stops_before_repair(duplicate, deepcopy(duplicate))

    def test_worker_preserves_native_budgets_and_exports_in_its_model_run(self):
        captured = {}

        class InertAgent:
            def __init__(self, model, env, **kwargs):
                captured["agent_settings"] = kwargs
                captured["model"] = model
                self.n_calls, self.cost = 2, 0.01234

            def run(self, **kwargs):
                captured["run_kwargs"] = kwargs
                return {"exit_status": "Submitted"}

        inert_environment = Mock()
        inert_environment.execute.return_value = {"returncode": 1, "output": "synthetic native script error"}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = driver.SPECS[0]
            task = tasks(1)[0]
            tdir = root / "runs" / spec["folder"] / "tasks" / task["case"]
            (tdir / "workspace").mkdir(parents=True)
            source = tdir / "workspace/buggy.py"
            source.write_text("# synthetic fixture, never executed\n", encoding="utf-8")
            task["hashes"]["buggy.py"] = hashlib.sha256(source.read_bytes()).hexdigest()
            (tdir / "agent_input.json").write_text(json.dumps({"title": "Synthetic question", "question": "Sanitized question"}), encoding="utf-8")
            with patch.object(driver, "ROOT", root), \
                 patch.object(driver, "DefaultAgent", InertAgent), \
                 patch.object(driver, "MonitoredBashEnvironment", return_value=inert_environment), \
                 patch.object(driver, "AnthropicMessagesModel", return_value=Mock()) as model_factory, \
                 patch.object(driver.adapter, "check_immutable") as immutable:
                result = driver.run_one(spec, task, config(), root / "api_queue")
            settings = captured["agent_settings"]
            self.assertEqual((settings["step_limit"], settings["cost_limit"], settings["wall_time_limit_seconds"]), (40, 1.0, 1200))
            self.assertEqual(settings["output_path"], tdir / "traj.json")
            self.assertNotIn("/work/buggy.py", settings["instance_template"])
            self.assertNotIn("intent", captured["run_kwargs"])
            self.assertFalse(captured["run_kwargs"]["mcp_enabled"])
            self.assertEqual(captured["run_kwargs"]["error_text"], "synthetic native script error")
            self.assertEqual(model_factory.call_args.kwargs["transport"].queue, root / "api_queue")
            self.assertEqual((tdir / "patched.py").read_bytes(), source.read_bytes())
            self.assertEqual(json.loads((tdir / "agent_result.json").read_text(encoding="utf-8")), result)
            self.assertFalse(result["candidate_test_feedback"])
            self.assertEqual(immutable.call_count, 2)
            inert_environment.execute.assert_called_once_with({"command": "$PY buggy.py"})

    def test_wrong_model_saved_artifact_cannot_be_silently_reused(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec, task = driver.SPECS[0], tasks(1)[0]
            tdir = root / "runs" / spec["folder"] / "tasks" / task["case"]
            tdir.mkdir(parents=True)
            (tdir / "agent_result.json").write_text(json.dumps({"case": task["case"], "model": "claude-haiku-4-5-20251001"}), encoding="utf-8")
            with patch.object(driver, "ROOT", root), \
                 patch.object(driver.adapter, "check_immutable"), \
                 self.assertRaises(ValueError):
                driver.run_one(spec, task, config(), root / "api_queue")

    def test_changed_saved_candidate_cannot_be_silently_reused(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec, task = driver.SPECS[0], tasks(1)[0]
            tdir = root / "runs" / spec["folder"] / "tasks" / task["case"]
            tdir.mkdir(parents=True)
            existing = {"case": task["case"], "version": task["version"], "model": spec["model"],
                        "candidate_sha256": "original generated digest"}
            (tdir / "agent_result.json").write_text(json.dumps(existing), encoding="utf-8")
            with patch.object(driver, "ROOT", root), \
                 patch.object(driver.adapter, "check_immutable"), \
                 patch.object(driver.adapter, "sha", return_value="tampered digest"), \
                 self.assertRaises(ValueError):
                driver.run_one(spec, task, config(), root / "api_queue")

    def _synthetic_summary_inputs(self, root):
        selected = tasks()
        for spec in driver.SPECS:
            run = root / "runs" / spec["folder"]
            driver.adapter.write_json(run / "manifest.json", {"count": 30, "tasks": selected})
            driver.adapter.write_json(run / "experiment.json", {"spec": spec, "status": "prepared"})
            for index, task in enumerate(selected):
                tdir = run / "tasks" / task["case"]
                driver.adapter.write_json(tdir / "agent_result.json", {"case": task["case"], "version": task["version"], "model": spec["model"],
                                                                      "candidate_sha256": "synthetic candidate digest",
                                                                      "submitted": index < 10, "exit_status": "Submitted" if index < 10 else "LimitsExceeded", "steps": 40, "cost_usd": 0.5})
                driver.adapter.write_json(tdir / "result.json", {"case": task["case"], "version": task["version"], "original": {"status": "FAIL"}, "reference": {"status": "PASS"}, "candidate": {"source_sha256": "synthetic candidate digest", "status": "PASS" if index < 20 else "FAIL"}, "repaired": index < 15})
        return selected

    def test_summary_rejects_wrong_model_or_inconsistent_submission(self):
        for change in [{"model": "claude-haiku-4-5-20251001"}, {"exit_status": "LimitsExceeded", "submitted": True}]:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                selected = self._synthetic_summary_inputs(root)
                path = root / "runs" / driver.SPECS[0]["folder"] / "tasks" / selected[0]["case"] / "agent_result.json"
                record = driver.adapter.read_json(path) | change
                driver.adapter.write_json(path, record)
                with patch.object(driver, "ROOT", root), self.assertRaises(ValueError):
                    driver.save_summaries(driver.SPECS)

    def test_summary_rejects_validation_of_a_different_candidate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            selected = self._synthetic_summary_inputs(root)
            path = root / "runs" / driver.SPECS[0]["folder"] / "tasks" / selected[0]["case"] / "result.json"
            record = driver.adapter.read_json(path)
            record["candidate"]["source_sha256"] = "different candidate digest"
            driver.adapter.write_json(path, record)
            with patch.object(driver, "ROOT", root), self.assertRaises(ValueError):
                driver.save_summaries(driver.SPECS)

    def test_summary_exports_correct_counts_and_distinguishes_actual_model(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._synthetic_summary_inputs(root)
            with patch.object(driver, "ROOT", root):
                result = driver.save_summaries(driver.SPECS)
            self.assertTrue(result["same_30_cases"])
            for spec, total in zip(driver.SPECS, result["models"]):
                self.assertEqual((total["cases"], total["test_pass"], total["repaired"], total["submitted_repaired"]), (30, 20, 15, 10))
                self.assertEqual(total["actual_model"], spec["model"])
                self.assertEqual(total["requested_model"], spec["requested"])
                self.assertEqual(total["cost_usd"], 15)
                self.assertTrue((root / "runs" / spec["folder"] / "model_summary.csv").is_file())
                self.assertTrue((root / (spec["folder"] + "_summary.csv")).is_file())
                self.assertEqual(driver.adapter.read_json(root / "runs" / spec["folder"] / "experiment.json")["status"], "complete")
            self.assertTrue((root / "claude_p30_comparison.csv").is_file())
            self.assertTrue((root / "reports/CLAUDE_P30_RESULTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
