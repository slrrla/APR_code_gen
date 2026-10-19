"""Mock Responses requests and actual DefaultAgent integration; no API/cases."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from minisweagent.agents.default import DefaultAgent
from minisweagent.exceptions import FormatError, Submitted

from claude_model import BASH_TOOL as CLAUDE_BASH_TOOL
from openai_model import BASH_TOOL, NativeResponseError, OpenAIResponsesModel, OpenAITokenPrices


MODEL = "gpt-6-astra"
PRICES = OpenAITokenPrices(input_per_million=2, output_per_million=10, cache_read_per_million=0.2)


def call(command="echo hello", call_id="call_mock"):
    return {"type": "function_call", "id": "fc_mock", "call_id": call_id, "name": "bash",
            "arguments": json.dumps({"command": command}), "status": "completed"}


def response(command="echo hello", *, output=None, usage=None, status="completed", model=MODEL, **kwargs):
    return {
        "id": "resp_mock", "object": "response", "model": model, "status": status,
        "created_at": 1000, "completed_at": 1001, "error": None, "incomplete_details": None,
        "output": output if output is not None else [call(command)],
        "usage": usage if usage is not None else {
            "input_tokens": 100, "input_tokens_details": {"cached_tokens": 0}, "output_tokens": 20,
            "output_tokens_details": {"reasoning_tokens": 8}, "total_tokens": 120,
        },
        **kwargs,
    }


class QueueTransport:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def __call__(self, payload):
        self.requests.append(deepcopy(payload))
        return deepcopy(self.responses.pop(0))


def model(transport, **kwargs):
    return OpenAIResponsesModel(MODEL, prices=PRICES, transport=transport, **kwargs)


class StubEnvironment:
    def __init__(self, submit=False):
        self.commands = []
        self.submit = submit

    def execute(self, action):
        self.commands.append(action["command"])
        if self.submit:
            raise Submitted({"role": "exit", "content": "Submitted",
                             "extra": {"exit_status": "Submitted", "submission": ""}})
        return {"output": "hello", "returncode": 0, "exception_info": ""}

    def get_template_vars(self):
        return {}

    def serialize(self):
        return {}


class OpenAIModelTests(unittest.TestCase):
    def test_original_prompts_native_output_and_observations_round_trip(self):
        native_output = [
            {"type": "reasoning", "id": "rs_mock", "summary": [], "encrypted_content": "opaque-reasoning"},
            {"type": "message", "id": "msg_mock", "role": "assistant", "status": "completed",
             "phase": "commentary", "content": [{"type": "output_text", "text": "Reproduce.", "annotations": []}]},
            call("$PY buggy.py"),
        ]
        transport = QueueTransport(response(output=native_output), response())
        client = model(transport)
        history = [{"role": "system", "content": "repair\n EXACT ", "extra": {"metadata": "excluded"}},
                   {"role": "user", "content": "Original\r\nquestion  "}]
        message = client.query(history)
        output = {"output": "error", "returncode": 1, "exception_info": "timeout", "extra": {"native_version": "pinned"}}
        observation = client.format_observation_messages(message, [output])[0]
        client.query(history + [message, observation])
        payload = transport.requests[1]
        self.assertEqual(payload["input"][:2], [{"role": m["role"], "content": m["content"]} for m in history])
        self.assertEqual(payload["input"][2:-1], native_output)
        self.assertEqual(payload["input"][-1], {"type": "function_call_output", "call_id": "call_mock",
                                               "output": "<returncode>1</returncode>\n<output>error</output>\n<exception>timeout</exception>"})
        self.assertEqual(message["content"], native_output)
        self.assertEqual(message["extra"]["response"]["output"], native_output)
        self.assertEqual(message["extra"]["response_created_at"], 1000)
        self.assertEqual(message["extra"]["response_completed_at"], 1001)
        self.assertEqual(message["extra"]["actions"], [{"command": "$PY buggy.py", "tool_call_id": "call_mock"}])
        self.assertEqual(observation["extra"]["native_version"], "pinned")
        self.assertNotIn("extra", payload["input"][-1])

    def test_fixed_protocol_and_tool_semantics_match_claude(self):
        transport = QueueTransport(response())
        model(transport).query([{"role": "user", "content": "task"}])
        payload = transport.requests[0]
        self.assertEqual(payload["tools"], [BASH_TOOL])
        self.assertEqual(BASH_TOOL["parameters"], CLAUDE_BASH_TOOL["input_schema"])
        self.assertEqual(BASH_TOOL["description"], CLAUDE_BASH_TOOL["description"])
        self.assertTrue(BASH_TOOL["strict"])
        self.assertEqual(payload["tool_choice"], "auto")
        self.assertFalse(payload["parallel_tool_calls"])
        self.assertFalse(payload["store"])
        self.assertEqual(payload["max_output_tokens"], 8192)
        self.assertEqual(payload["include"], ["reasoning.encrypted_content"])
        for key in ("reasoning", "temperature", "previous_response_id", "api_key"):
            self.assertNotIn(key, payload)

    def test_transport_is_required_and_credentials_never_loaded(self):
        with self.assertRaises(TypeError):
            OpenAIResponsesModel(MODEL, prices=PRICES)
        with patch("os.getenv", side_effect=AssertionError("Worker accessed an environment variable")):
            client = model(QueueTransport(response()))
            client.query([{"role": "user", "content": "task"}])
        self.assertFalse(hasattr(client, "_api_key"))
        self.assertNotIn("api_key", json.dumps(client.serialize()))

    def test_cache_and_reasoning_usage_are_charged_exactly_once(self):
        usage = {"input_tokens": 100, "input_tokens_details": {"cached_tokens": 50},
                 "output_tokens": 20, "output_tokens_details": {"reasoning_tokens": 15}, "total_tokens": 120}
        message = model(QueueTransport(response(usage=usage))).query([{"role": "user", "content": "task"}])
        self.assertAlmostEqual(message["extra"]["cost"], 0.00031)
        self.assertEqual(message["extra"]["usage"], usage)
        self.assertEqual(message["extra"]["cost_status"], "priced")

    def test_cache_pricing_must_be_explicit_when_usage_is_reported(self):
        with self.assertRaisesRegex(ValueError, "cached-input"):
            OpenAITokenPrices(2, 10).cost({"input_tokens": 100, "output_tokens": 5, "input_tokens_details": {"cached_tokens": 50}})
        with self.assertRaisesRegex(ValueError, "cache-write"):
            PRICES.cost({"input_tokens": 100, "output_tokens": 5, "input_tokens_details": {"cache_write_tokens": 20}})
        prices = OpenAITokenPrices(2, 10, 0.2, 3)
        self.assertAlmostEqual(prices.cost({"input_tokens": 100, "output_tokens": 20,
                                           "input_tokens_details": {"cached_tokens": 50, "cache_write_tokens": 20}}), 0.00033)
        self.assertEqual(prices.cost({"input_tokens": 100, "output_tokens": 20}), PRICES.cost({"input_tokens": 100, "output_tokens": 20}))

    def test_usage_and_prices_fail_closed(self):
        bad_usage = [
            {}, {"output_tokens": 1}, {"input_tokens": -1, "output_tokens": 1},
            {"input_tokens": True, "output_tokens": 1}, {"input_tokens": 10, "output_tokens": 1, "total_tokens": 99},
            {"input_tokens": 10, "output_tokens": 1, "input_tokens_details": {"cached_tokens": 11}},
            {"input_tokens": 10, "output_tokens": 1, "output_tokens_details": {"reasoning_tokens": 2}},
            {"input_tokens": 10, "output_tokens": 1, "input_tokens_details": []},
            {"input_tokens": 10, "output_tokens": 1, "output_tokens_details": False},
        ]
        for usage in bad_usage:
            with self.subTest(usage=usage), self.assertRaises(ValueError):
                PRICES.cost(usage)
        for price in (-1, True, float("inf"), float("nan")):
            with self.subTest(price=price), self.assertRaises(ValueError):
                OpenAITokenPrices(price, 10)

    def test_long_context_premium_starts_above_boundary_for_entire_request(self):
        prices = OpenAITokenPrices(10, 50, 1, 12.5)
        usage = {"input_tokens": 272_000, "output_tokens": 100,
                 "input_tokens_details": {"cached_tokens": 100_000, "cache_write_tokens": 20_000}}
        # Exact boundary: 152K ordinary + 100K cached + 20K written at normal rates.
        self.assertAlmostEqual(prices.cost(usage), (152_000 * 10 + 100_000 + 20_000 * 12.5 + 100 * 50) / 1_000_000)
        usage["input_tokens"] += 1
        # One token over doubles the entire input/cache cost, and all output is 1.5x.
        self.assertAlmostEqual(prices.cost(usage),
                               ((152_001 * 10 + 100_000 + 20_000 * 12.5) * 2 + 100 * 50 * 1.5) / 1_000_000)
        self.assertEqual(model(QueueTransport()).serialize()["info"]["config"]["model"]["prices"][
            "long_context_threshold_input_tokens"], 272_000)

    def test_long_context_pricing_configuration_is_validated(self):
        for threshold in (0, -1, True, 272000.5):
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                OpenAITokenPrices(2, 10, long_context_threshold_input_tokens=threshold)
        for multiplier in (-1, True, float("inf"), float("nan")):
            with self.subTest(multiplier=multiplier), self.assertRaises(ValueError):
                OpenAITokenPrices(2, 10, long_context_input_multiplier=multiplier)

    def test_malformed_arguments_are_billed_and_do_not_produce_actions(self):
        for args in ('{"command":5}', '{"command":" "}', '{"command":"x","extra":1}',
                     '{"command":"x","command":"y"}', '{}', 'not JSON', None):
            with self.subTest(args=args):
                item = call()
                item["arguments"] = args
                native = response(output=[item])
                with self.assertRaises(FormatError) as caught:
                    model(QueueTransport(native)).query([{"role": "user", "content": "task"}])
                assistant, feedback = caught.exception.messages
                self.assertEqual(assistant["extra"]["response"], native)
                self.assertAlmostEqual(assistant["extra"]["cost"], 0.0004)
                self.assertNotIn("actions", assistant["extra"])
                self.assertEqual(feedback["content"][0]["call_id"], "call_mock")

    def test_multiple_calls_receive_outputs_without_any_execution(self):
        with self.assertRaises(FormatError) as caught:
            model(QueueTransport(response(output=[call("one", "one"), call("two", "two")]))).query([])
        assistant, feedback = caught.exception.messages
        self.assertNotIn("actions", assistant["extra"])
        self.assertEqual([item["call_id"] for item in feedback["content"]], ["one", "two"])
        transport = QueueTransport(response())
        model(transport).query([assistant, feedback])
        self.assertEqual([item["type"] for item in transport.requests[0]["input"]],
                         ["function_call", "function_call", "function_call_output", "function_call_output"])

    def test_incomplete_response_is_billed_even_when_call_looks_complete(self):
        native = response(status="incomplete", incomplete_details={"reason": "max_output_tokens"})
        with self.assertRaises(FormatError) as caught:
            model(QueueTransport(native)).query([])
        assistant, feedback = caught.exception.messages
        self.assertAlmostEqual(assistant["extra"]["cost"], 0.0004)
        self.assertNotIn("actions", assistant["extra"])
        self.assertIn("token limit", feedback["content"][0]["output"])

    def test_unknown_function_and_incomplete_call_never_execute(self):
        wrong_name, incomplete_call = call(), call()
        wrong_name["name"] = "other"
        incomplete_call["status"] = "in_progress"
        for item in (wrong_name, incomplete_call):
            with self.subTest(item=item), self.assertRaises(FormatError) as caught:
                model(QueueTransport(response(output=[item]))).query([])
            self.assertNotIn("actions", caught.exception.messages[0]["extra"])
            self.assertEqual(caught.exception.messages[1]["content"][0]["call_id"], "call_mock")

    def test_malformed_native_details_retain_billed_response(self):
        native = response(status="incomplete", incomplete_details=["invalid"])
        with self.assertRaises(NativeResponseError) as caught:
            model(QueueTransport(native)).query([])
        self.assertEqual(caught.exception.messages[0]["extra"]["response"], native)
        self.assertAlmostEqual(caught.exception.messages[0]["extra"]["cost"], 0.0004)

    def test_missing_or_duplicate_native_ids_stop_with_billed_record(self):
        missing_id = call()
        missing_id.pop("call_id")
        for output in ([missing_id], [call(), call()]):
            with self.subTest(output=output), self.assertRaises(NativeResponseError) as caught:
                model(QueueTransport(response(output=output))).query([])
            self.assertEqual(caught.exception.messages[-1]["role"], "exit")
            self.assertAlmostEqual(caught.exception.messages[0]["extra"]["cost"], 0.0004)

    def test_snapshot_requires_explicit_recorded_allowlist(self):
        snapshot = MODEL + "-2026-10-01"
        with self.assertRaises(NativeResponseError) as caught:
            model(QueueTransport(response(model=snapshot))).query([])
        self.assertEqual(caught.exception.messages[0]["extra"]["cost_status"], "requested_model_rate_only")
        client = model(QueueTransport(response(model=snapshot)), accepted_response_models=(snapshot,))
        self.assertEqual(client.query([])["extra"]["response"]["model"], snapshot)
        self.assertEqual(client.serialize()["info"]["config"]["model"]["accepted_response_models"], [snapshot])

    def test_failed_provider_response_stops_and_retains_returned_usage(self):
        transport = QueueTransport(response(status="failed", error={"code": "server_error", "message": "failed"}))
        env = StubEnvironment()
        agent = DefaultAgent(model(transport), env, system_template="repair", instance_template="task", step_limit=3)
        self.assertEqual(agent.run()["exit_status"], "NativeResponseError")
        self.assertAlmostEqual(agent.cost, 0.0004)
        self.assertEqual(agent.n_calls, 1)
        self.assertEqual(env.commands, [])
        self.assertEqual(agent.messages[-2]["extra"]["response"]["status"], "failed")

    def test_missing_usage_is_explicitly_unknown_and_stops_before_execution(self):
        native = response()
        native["usage"] = None
        env = StubEnvironment()
        agent = DefaultAgent(model(QueueTransport(native)), env, system_template="repair", instance_template="task")
        self.assertEqual(agent.run()["exit_status"], "NativeResponseError")
        self.assertEqual(agent.messages[-2]["extra"]["cost_status"], "unknown")
        self.assertIsNone(agent.messages[-2]["extra"]["usage"])
        self.assertEqual(env.commands, [])

    def test_actual_default_agent_bills_format_error_then_submits(self):
        text_output = [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Forgot tool", "annotations": []}]}]
        transport = QueueTransport(response(output=text_output), response("echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"))
        env = StubEnvironment(submit=True)
        agent = DefaultAgent(model(transport), env, system_template="repair", instance_template="task",
                             step_limit=3, cost_limit=1, wall_time_limit_seconds=10)
        result = agent.run()
        self.assertEqual(result["exit_status"], "Submitted")
        self.assertEqual(agent.n_calls, 2)
        self.assertAlmostEqual(agent.cost, 0.0008)
        self.assertEqual(env.commands, ["echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"])
        self.assertEqual(transport.requests[1]["input"][2], text_output[0])
        self.assertEqual(agent.serialize()["info"]["model_stats"]["api_calls"], 2)

    def test_actual_default_agent_step_and_cost_limits_apply(self):
        for steps, cost_limit in ((1, 1), (5, 0.0003)):
            with self.subTest(steps=steps, cost_limit=cost_limit):
                transport = QueueTransport(response())
                env = StubEnvironment()
                agent = DefaultAgent(model(transport), env, system_template="repair", instance_template="task",
                                     step_limit=steps, cost_limit=cost_limit)
                self.assertEqual(agent.run()["exit_status"], "LimitsExceeded")
                self.assertEqual(agent.n_calls, 1)
                self.assertAlmostEqual(agent.cost, 0.0004)
                self.assertEqual(len(transport.requests), 1)


if __name__ == "__main__":
    unittest.main()
