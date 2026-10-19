"""Offline broker tests. HTTP and API credentials are synthetic throughout."""
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error

import openai_api_broker as broker


KEY = "sk-synthetic-broker-test-value"


def payload(**changes):
    value = {"model": "gpt-6-sol", "input": [{"role": "user", "content": "Repair the script."}],
             "tools": [deepcopy(broker.BASH_TOOL)], "tool_choice": "auto", "parallel_tool_calls": False,
             "max_output_tokens": 8192, "store": False, "include": ["reasoning.encrypted_content"]}
    value.update(changes)
    return value


def success(**changes):
    value = {"id": "resp_synthetic", "object": "response", "model": "gpt-6-sol", "output": [],
             "usage": {"input_tokens": 3, "output_tokens": 2, "total_tokens": 5}}
    value.update(changes)
    return value


def http_response(value):
    return io.BytesIO(json.dumps(value).encode("utf-8"))


def http_error(status, message="Rejected", retry="0"):
    return urllib.error.HTTPError(broker.RESPONSES_URL, status, "API error", {"Retry-After": retry},
                                  http_response({"error": {"type": "api_error", "message": message}}))


def preflight_success():
    return {"ok": True, "checked_at": "2026-10-08T00:00:00+00:00", "availability": {model: True for model in broker.MODELS},
            "accepted_response_models": {model: [model] for model in broker.MODELS}}


class BrokerTests(unittest.TestCase):
    def setUp(self):
        temporary_root = broker.ROOT / "records" / "gpt_p30_test_tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.opener = Mock()
        self.open_patch = patch.object(broker.urllib.request, "build_opener", return_value=self.opener)
        self.open_patch.start()
        self.addCleanup(self.open_patch.stop)

    def test_native_response_and_fixed_network_endpoint(self):
        self.opener.open.return_value = http_response(success())
        self.assertEqual(broker.api_request(payload(), KEY), success())
        request = self.opener.open.call_args.args[0]
        self.assertEqual(request.full_url, broker.RESPONSES_URL)
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer " + KEY)
        self.assertEqual(json.loads(request.data), payload())

    def test_redirects_do_not_forward_authorization(self):
        self.assertIsNone(broker._NoRedirect().redirect_request(None, None, 302, "redirect", {}, "https://example.invalid/"))
        self.opener.open.side_effect = http_error(302)
        self.assertEqual(broker.api_request(payload(), KEY)["http_status"], 302)
        self.assertEqual(self.opener.open.call_count, 1)

    def test_arbitrary_endpoint_is_rejected_before_network(self):
        result = broker._request_json("https://example.invalid/v1/responses", KEY, payload())
        self.assertEqual(result["error"]["type"], "unauthorized_endpoint")
        self.opener.open.assert_not_called()

    def test_payload_rejections_do_not_touch_network(self):
        invalid = [None, [], payload(model="gpt-6.1-sol"), payload(base_url="https://example.invalid"),
                   payload(tools=[{"type": "web_search"}]), payload(tool_choice="required"),
                   payload(parallel_tool_calls=True), payload(store=True), payload(max_output_tokens=8193),
                   payload(max_output_tokens=True), payload(include=["message.output_text.logprobs"]),
                   payload(input=[{"type": "computer_call"}]), payload(reasoning={"summary": "auto"})]
        for value in invalid:
            with self.subTest(value=value):
                self.assertIn("error", broker.api_request(value, KEY))
        self.opener.open.assert_not_called()

    def test_exact_function_schema_is_required(self):
        changed = payload()
        changed["tools"][0]["parameters"]["additionalProperties"] = True
        self.assertIn("error", broker.api_request(changed, KEY))
        self.opener.open.assert_not_called()

    def test_native_input_types_and_encrypted_reasoning_replay(self):
        inputs = [{"role": "system", "content": "repair"},
                  {"role": "user", "content": [{"type": "input_text", "text": "task"}]},
                  {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Reason", "annotations": []}]},
                  {"type": "reasoning", "id": "rs_1", "summary": [], "encrypted_content": "opaque"},
                  {"type": "function_call", "id": "fc_1", "name": "bash", "call_id": "call_1", "arguments": "{\"command\":\"pwd\"}"},
                  {"type": "function_call_output", "call_id": "call_1", "output": "workspace"}]
        self.assertIsNone(broker.validate_payload(payload(input=inputs)))
        self.assertIsNone(broker.validate_payload(payload(input="plain prompt")))
        self.assertIsNone(broker.validate_payload(payload(reasoning={"effort": "high"})))

    def test_input_malformed_or_nontext_content_is_rejected(self):
        for value in [[{"role": "tool", "content": "x"}], [{"role": "user", "content": [{"type": "input_image", "image_url": "x"}]}],
                      [{"type": "function_call", "name": "other", "call_id": "c", "arguments": "{}"}],
                      [{"type": "function_call_output", "call_id": "c", "output": 1}],
                      [{"type": "reasoning", "encrypted_content": {}}]]:
            with self.subTest(value=value):
                self.assertIsNotNone(broker.validate_payload(payload(input=value)))

    def test_rate_limit_and_service_rejection_retry_are_bounded(self):
        self.opener.open.side_effect = [http_error(429, retry="999"), http_error(503, retry="invalid"), http_response(success())]
        with patch.object(broker.time, "sleep") as sleep:
            self.assertEqual(broker.api_request(payload(), KEY), success())
        self.assertEqual(self.opener.open.call_count, 3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [30.0, 5.0])

    def test_rate_limit_exhaustion_never_tries_a_fourth_call(self):
        self.opener.open.side_effect = [http_error(429) for _ in range(3)]
        with patch.object(broker.time, "sleep"):
            self.assertEqual(broker.api_request(payload(), KEY)["http_status"], 429)
        self.assertEqual(self.opener.open.call_count, 3)

    def test_timeout_and_other_server_errors_are_not_retried(self):
        for error in [TimeoutError("lost response"), urllib.error.URLError("lost connection"), http_error(500), http_error(401)]:
            with self.subTest(error=type(error).__name__):
                self.opener.open.reset_mock()
                self.opener.open.side_effect = error
                self.assertIn("error", broker.api_request(payload(), KEY))
                self.assertEqual(self.opener.open.call_count, 1)

    def test_errors_and_success_content_are_key_redacted(self):
        for error in [http_error(401, "invalid " + KEY), RuntimeError("bad " + KEY)]:
            self.opener.open.side_effect = error
            self.assertNotIn(KEY, json.dumps(broker.api_request(payload(), KEY)))
        self.opener.open.side_effect = None
        self.opener.open.return_value = http_response(success(output=[{"text": KEY}]))
        self.assertEqual(broker.api_request(payload(), KEY)["output"][0]["text"], "[REDACTED]")

    def test_mismatched_model_retains_native_usage_without_retry(self):
        native = success(model="different-model")
        self.opener.open.return_value = http_response(native)
        result = broker.api_request(payload(), KEY)
        self.assertEqual(result["error"]["type"], "model_mismatch")
        self.assertEqual(result["native_response"], native)
        self.assertEqual(self.opener.open.call_count, 1)

    def test_native_error_null_does_not_skip_model_verification(self):
        native = success(model="different-model", error=None)
        self.opener.open.return_value = http_response(native)
        result = broker.api_request(payload(), KEY)
        self.assertEqual(result["error"]["type"], "model_mismatch")
        self.assertEqual(result["native_response"], native)

    def test_failed_native_response_retains_usage_and_error_for_adapter_accounting(self):
        native = success(status="failed", error={"code": "server_error", "message": "Generation failed"})
        self.opener.open.return_value = http_response(native)
        result = broker.api_request(payload(), KEY)
        self.assertEqual(result, native)
        self.assertEqual(result["usage"]["total_tokens"], 5)
        self.assertEqual(self.opener.open.call_count, 1)

    def test_only_explicitly_preflighted_matching_snapshot_is_accepted(self):
        dated = "gpt-6-sol-2026-10-08"
        for accepted, allowed in [(None, False), ({"gpt-6-sol": [dated]}, True), ({"gpt-6-sol": ["gpt-6-astra"]}, False)]:
            self.opener.open.return_value = http_response(success(model=dated))
            result = broker.api_request(payload(), KEY, accepted)
            self.assertEqual("error" not in result, allowed)

    def test_preflight_get_has_only_requested_model_metadata(self):
        data = [{"id": model, "object": "model", "created": 1, "owned_by": "openai", "ignored": "x"} for model in broker.MODELS]
        data.extend([{"id": "gpt-6-sol-2026-10-08"}, {"id": "unrelated-model"}])
        self.opener.open.return_value = http_response({"data": data})
        result = broker.preflight(KEY)
        self.assertTrue(result["ok"])
        self.assertEqual(len(result["models"]), 4)
        self.assertNotIn("ignored", json.dumps(result))
        request = self.opener.open.call_args.args[0]
        self.assertEqual(request.full_url, broker.MODELS_URL)
        self.assertEqual(request.get_method(), "GET")
        self.assertIsNone(request.data)

    def test_preflight_does_not_silently_substitute_an_alias(self):
        self.opener.open.return_value = http_response({"data": [{"id": model + "-2026-10-08"} for model in broker.MODELS]})
        result = broker.preflight(KEY)
        self.assertFalse(result["ok"])
        self.assertFalse(any(result["availability"].values()))

    def test_environment_and_windows_user_fallback(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": KEY}), patch.object(broker, "_windows_user_key") as user_key:
            self.assertEqual(broker.load_key(), KEY)
            user_key.assert_not_called()
        with patch.dict(os.environ, {}, clear=True), patch.object(broker, "_windows_user_key", return_value=KEY):
            self.assertEqual(broker.load_key(), KEY)

    def test_key_file_plain_env_and_hidden_prompt(self):
        source = self.directory / "key.env"
        for content in [KEY, "\ufeff" + KEY, "# ignored\nOPENAI_API_KEY=" + KEY,
                        "export OPENAI_API_KEY='" + KEY + "'", "OPENAI_API_KEY=\"" + KEY + "\"\nUNRELATED=ignored"]:
            source.write_text(content, encoding="utf-8")
            self.assertEqual(broker.load_key(source), KEY)
        with patch.object(broker.getpass, "getpass", return_value=KEY) as prompt:
            self.assertEqual(broker.load_key(prompt_key=True), KEY)
            prompt.assert_called_once()
        self.assertTrue(source.exists())

    def test_key_loader_failures_never_echo_secrets(self):
        source = self.directory / "key.env"
        for content in ["OPENAI_API_KEY=" + KEY + "\nOPENAI_API_KEY=" + KEY, "OTHER=" + KEY, KEY + "\ninvalid"]:
            source.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                broker.load_key(source)
            self.assertNotIn(KEY, str(caught.exception))
        with self.assertRaises(ValueError):
            broker.load_key(source, True)

    def test_atomic_json_and_claim_are_durable_and_exclusive(self):
        destination = self.directory / "response.json"
        broker.atomic_json(destination, {"answer": 1})
        broker.atomic_json(destination, {"answer": 2})
        self.assertEqual(json.loads(destination.read_text()), {"answer": 2})
        self.assertEqual(list(self.directory.glob("*.tmp")), [])
        claim = self.directory / "claim.json"
        self.assertTrue(broker._claim(claim, "gpt-6-sol"))
        first = claim.read_bytes()
        self.assertFalse(broker._claim(claim, "gpt-6-sol"))
        self.assertEqual(first, claim.read_bytes())

    def _serve_until_responses(self, expected, api_mock):
        loops = 0
        original_sleep = broker.time.sleep

        def tick(_):
            nonlocal loops
            loops += 1
            if all((self.directory / (name + ".response.json")).exists() for name in expected):
                (self.directory / "stop").touch()
            if loops > 100:
                raise AssertionError("Mock broker did not finish")
            original_sleep(0.001)

        with patch.object(broker, "preflight", return_value=preflight_success()), \
             patch.object(broker, "PREFLIGHT_PATH", self.directory / "preflight.json"), \
             patch.object(broker, "api_request", api_mock), patch.object(broker.time, "sleep", side_effect=tick):
            return broker.serve(self.directory, KEY)

    def test_queue_completed_and_previously_claimed_requests_never_replay(self):
        completed, claimed, fresh = "a" * 32, "b" * 32, "c" * 32
        for name in (completed, claimed, fresh):
            broker.atomic_json(self.directory / (name + ".request.json"), payload())
        broker.atomic_json(self.directory / (completed + ".response.json"), {"retained": True})
        broker.atomic_json(self.directory / (claimed + ".claimed.json"), {"claimed": True})
        api = Mock(return_value=success())
        result = self._serve_until_responses((completed, claimed, fresh), api)
        self.assertTrue(result["stopped"])
        api.assert_called_once()
        self.assertEqual(json.loads((self.directory / (completed + ".response.json")).read_text()), {"retained": True})
        self.assertEqual(json.loads((self.directory / (claimed + ".response.json")).read_text())["error"]["type"], "ambiguous_previous_request")
        startup = json.loads((self.directory / "startup.json").read_text())
        self.assertTrue(startup["preflight_ok"])
        self.assertEqual(len(startup["broker_source_sha256"]), 64)
        self.assertFalse((self.directory / "ready.json").exists())

    def test_queue_malformed_and_unauthorized_requests_do_not_reach_api(self):
        malformed, bad = "d" * 32, "e" * 32
        (self.directory / (malformed + ".request.json")).write_text("{broken", encoding="utf-8")
        broker.atomic_json(self.directory / (bad + ".request.json"), payload(model="other"))
        api = Mock()
        self._serve_until_responses((malformed, bad), api)
        api.assert_not_called()
        self.assertEqual(list(self.directory.glob("*.claimed.json")), [])

    def test_failed_preflight_never_announces_ready_or_submits_requests(self):
        (self.directory / "ready.json").write_text("{}")
        with patch.object(broker, "preflight", return_value={"ok": False, "error": {"type": "missing_models"}}), \
             patch.object(broker, "PREFLIGHT_PATH", self.directory / "preflight.json"), patch.object(broker, "api_request") as api:
            self.assertFalse(broker.serve(self.directory, KEY)["ok"])
        self.assertFalse((self.directory / "ready.json").exists())
        api.assert_not_called()

    def test_existing_stop_prevents_new_requests(self):
        broker.atomic_json(self.directory / ("f" * 32 + ".request.json"), payload())
        (self.directory / "stop").touch()
        with patch.object(broker, "preflight", return_value=preflight_success()), \
             patch.object(broker, "PREFLIGHT_PATH", self.directory / "preflight.json"), patch.object(broker, "api_request") as api:
            result = broker.serve(self.directory, KEY)
        self.assertEqual(result["requests_seen"], 0)
        api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
