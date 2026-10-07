"""Mocked native API and actual DefaultAgent contract tests; no case inputs."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from minisweagent.agents.default import DefaultAgent
from minisweagent.exceptions import FormatError, Submitted

from claude_model import AnthropicMessagesModel, TokenPrices


PRICES = TokenPrices(2, 10, 2.5, 0.2)


def response(command="echo hello", *, content=None, usage=None, stop_reason="tool_use"):
    return {
        "id": "msg_mock",
        "type": "message",
        "role": "assistant",
        "model": "claude-sonnet-5-5",
        "content": content if content is not None else [
            {"type": "tool_use", "id": "toolu_mock", "name": "bash", "input": {"command": command}},
        ],
        "stop_reason": stop_reason,
        "stop_sequence": None,
        "usage": usage if usage is not None else {"input_tokens": 100, "output_tokens": 20},
    }


class QueueTransport:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def __call__(self, payload):
        self.requests.append(deepcopy(payload))
        return deepcopy(self.responses.pop(0))


def model(transport, **kwargs):
    return AnthropicMessagesModel("claude-sonnet-5-5", prices=PRICES, transport=transport, **kwargs)


class ModelTests(unittest.TestCase):
    def test_native_thinking_and_tool_results_round_trip_without_metadata(self):
        content = [
            {"type": "thinking", "thinking": "Consider the bug", "signature": "opaque-signature"},
            {"type": "redacted_thinking", "data": "opaque-data"},
            {"type": "text", "text": "Reproduce the error."},
            {"type": "tool_use", "id": "toolu_mock", "name": "bash", "input": {"command": "$PY buggy.py"}},
        ]
        transport = QueueTransport(response(content=content), response())
        client = model(transport)
        history = [{"role": "system", "content": "repair", "extra": {"private": "metadata"}},
                   {"role": "user", "content": "task"}]
        message = client.query(history)
        observation = client.format_observation_messages(
            message, [{"output": "failure", "returncode": 1, "exception_info": ""}]
        )[0]
        client.query(history + [message, observation])
        payload = transport.requests[1]
        self.assertEqual(payload["messages"][-2], {"role": "assistant", "content": content})
        self.assertEqual(payload["messages"][-1]["content"][0]["tool_use_id"], "toolu_mock")
        self.assertNotIn("extra", payload["messages"][-1])
        self.assertEqual(payload["system"], [{"type": "text", "text": "repair"}])
        self.assertEqual(payload["tool_choice"], {"type": "auto", "disable_parallel_tool_use": True})
        self.assertTrue(payload["tools"][0]["strict"])
        self.assertFalse(payload["tools"][0]["input_schema"]["additionalProperties"])
        self.assertEqual(message["extra"]["actions"], [{"command": "$PY buggy.py", "tool_call_id": "toolu_mock"}])

    def test_broker_transport_does_not_read_or_serialize_credentials(self):
        with patch("claude_model.os.getenv", side_effect=AssertionError("Worker read an environment variable")):
            client = model(QueueTransport(response()), api_key="must-not-be-retained")
        self.assertIsNone(client._api_key)
        client.query([{"role": "user", "content": "task"}])
        self.assertNotIn("must-not-be-retained", json.dumps(client.serialize()))

    def test_native_usage_cost_includes_cache_tokens_once(self):
        usage = {"input_tokens": 100, "output_tokens": 20,
                 "cache_creation_input_tokens": 20, "cache_read_input_tokens": 50}
        message = model(QueueTransport(response(usage=usage))).query([{"role": "user", "content": "task"}])
        self.assertAlmostEqual(message["extra"]["cost"], 0.00046)
        self.assertEqual(message["extra"]["usage"], usage)

    def test_one_hour_cache_price_requires_explicit_value(self):
        usage = {"input_tokens": 0, "output_tokens": 0, "cache_creation_input_tokens": 30,
                 "cache_creation": {"ephemeral_5m_input_tokens": 10, "ephemeral_1h_input_tokens": 20}}
        with self.assertRaisesRegex(ValueError, "one-hour"):
            PRICES.cost(usage)
        self.assertAlmostEqual(TokenPrices(2, 10, 2.5, 0.2, 4).cost(usage), 0.000105)

    def test_invalid_bash_input_retains_billed_response_without_action(self):
        for args in ({"command": 5}, {"command": " "}, {"command": "echo x", "other": 1}, {}):
            with self.subTest(args=args):
                native = response(content=[{"type": "tool_use", "id": "toolu_mock", "name": "bash", "input": args}])
                with self.assertRaises(FormatError) as raised:
                    model(QueueTransport(native)).query([{"role": "user", "content": "task"}])
                assistant, feedback = raised.exception.messages
                self.assertEqual(assistant["extra"]["response"], native)
                self.assertAlmostEqual(assistant["extra"]["cost"], 0.0004)
                self.assertNotIn("actions", assistant["extra"])
                self.assertTrue(feedback["content"][0]["is_error"])
                self.assertEqual(feedback["content"][0]["tool_use_id"], "toolu_mock")

    def test_multiple_tools_are_rejected_and_all_ids_receive_errors(self):
        tools = [
            {"type": "tool_use", "id": "one", "name": "bash", "input": {"command": "echo one"}},
            {"type": "tool_use", "id": "two", "name": "bash", "input": {"command": "echo two"}},
        ]
        with self.assertRaises(FormatError) as raised:
            model(QueueTransport(response(content=tools))).query([{"role": "user", "content": "task"}])
        self.assertEqual([b["tool_use_id"] for b in raised.exception.messages[1]["content"]], ["one", "two"])

    def test_output_truncation_is_not_executed(self):
        with self.assertRaises(FormatError) as raised:
            model(QueueTransport(response(stop_reason="max_tokens"))).query([{"role": "user", "content": "task"}])
        self.assertNotIn("actions", raised.exception.messages[0]["extra"])
        self.assertIn("token limit", raised.exception.messages[1]["content"][0]["content"])

    def test_payload_cannot_override_agent_tools_or_model(self):
        for key in ("tools", "messages", "model", "tool_choice", "api_key", "drop_params"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                model(QueueTransport(response()), model_kwargs={key: "override"})

    def test_usage_validation_fails_closed(self):
        for usage in ({"output_tokens": 5}, {"input_tokens": -1, "output_tokens": 5},
                      {"input_tokens": True, "output_tokens": 5}):
            with self.subTest(usage=usage), self.assertRaises(ValueError):
                PRICES.cost(usage)

    def test_actual_default_agent_bills_format_errors_and_submits(self):
        class Env:
            def __init__(self):
                self.commands = []

            def execute(self, action):
                self.commands.append(action["command"])
                raise Submitted({"role": "exit", "content": "Submitted",
                                 "extra": {"exit_status": "Submitted", "submission": ""}})

            def get_template_vars(self):
                return {}

            def serialize(self):
                return {}

        transport = QueueTransport(
            response(content=[{"type": "text", "text": "Forgot the tool"}], stop_reason="end_turn"),
            response("echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"),
        )
        env = Env()
        agent = DefaultAgent(model(transport), env, system_template="repair", instance_template="task",
                             step_limit=3, cost_limit=1, wall_time_limit_seconds=10)
        result = agent.run()
        self.assertEqual(result["exit_status"], "Submitted")
        self.assertEqual(agent.n_calls, 2)
        self.assertAlmostEqual(agent.cost, 0.0008)
        self.assertEqual(env.commands, ["echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"])
        self.assertEqual(transport.requests[1]["messages"][-2]["content"], [{"type": "text", "text": "Forgot the tool"}])

    def test_actual_default_agent_stops_before_next_call_at_step_or_cost_limit(self):
        class Env:
            def execute(self, action):
                return {"output": "hello", "returncode": 0, "exception_info": ""}

            def get_template_vars(self):
                return {}

            def serialize(self):
                return {}

        for step_limit, cost_limit in ((1, 1), (5, 0.0003)):
            with self.subTest(step_limit=step_limit, cost_limit=cost_limit):
                transport = QueueTransport(response())
                agent = DefaultAgent(model(transport), Env(), system_template="repair", instance_template="task",
                                     step_limit=step_limit, cost_limit=cost_limit)
                self.assertEqual(agent.run()["exit_status"], "LimitsExceeded")
                self.assertEqual(len(transport.requests), 1)
                self.assertEqual(agent.n_calls, 1)
                self.assertAlmostEqual(agent.cost, 0.0004)


if __name__ == "__main__":
    unittest.main()
