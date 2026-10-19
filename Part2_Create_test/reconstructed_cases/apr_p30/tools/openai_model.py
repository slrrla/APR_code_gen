"""Credential-free Responses API model for mini-swe-agent's DefaultAgent.

The injected ``transport(payload) -> response`` owns authentication and network
access. Native output items, including encrypted reasoning, are retained in the
trajectory and replayed with function outputs in each stateless request.

Protocol references:
https://developers.openai.com/api/docs/guides/function-calling
https://developers.openai.com/api/docs/guides/reasoning
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import json
import math
import time
from typing import Any, Callable

from jinja2 import StrictUndefined, Template
from minisweagent.exceptions import FormatError

from claude_model import DEFAULT_FORMAT_ERROR, DEFAULT_OBSERVATION


BASH_TOOL = {
    "type": "function",
    "name": "bash",
    "description": "Execute one bash command in the repair workspace.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
        "additionalProperties": False,
    },
}


@dataclass(frozen=True)
class OpenAITokenPrices:
    """Explicit USD per million tokens; cached input is part of input_tokens.

    No cache writes are inferred from uncached tokens. The optional write price
    applies to the native ``input_tokens_details.cache_write_tokens`` counter.
    Reasoning tokens are already included in output_tokens and are not rebilled.
    The default long-context threshold/multipliers are the published Standard
    rates for GPT-6 Astra, Luna, and Sol: requests exceeding 272K input tokens
    charge all input/cache tokens at 2x and output tokens at 1.5x.

    https://developers.openai.com/api/docs/guides/prompt-caching
    https://developers.openai.com/api/docs/models/gpt-6-astra
    https://developers.openai.com/api/docs/models/gpt-6-luna
    https://developers.openai.com/api/docs/models/gpt-6-sol
    """

    input_per_million: float
    output_per_million: float
    cache_read_per_million: float | None = None
    cache_write_per_million: float | None = None
    long_context_threshold_input_tokens: int = 272_000
    long_context_input_multiplier: float = 2.0
    long_context_output_multiplier: float = 1.5

    def __post_init__(self) -> None:
        threshold = self.long_context_threshold_input_tokens
        if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 1:
            raise ValueError("Long-context input threshold must be a positive integer")
        for name, value in asdict(self).items():
            if name.startswith("cache_") and value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"Invalid token price: {name}")

    def cost(self, usage: dict) -> float:
        if not isinstance(usage, dict) or "input_tokens" not in usage or "output_tokens" not in usage:
            raise ValueError("OpenAI response is missing input/output usage")

        def count(data: dict, key: str) -> int:
            value = data.get(key, 0)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"Invalid OpenAI usage count: {key}")
            return value

        input_tokens, output_tokens = count(usage, "input_tokens"), count(usage, "output_tokens")
        details = usage.get("input_tokens_details", {})
        output_details = usage.get("output_tokens_details", {})
        details = {} if details is None else details
        output_details = {} if output_details is None else output_details
        if not isinstance(details, dict) or not isinstance(output_details, dict):
            raise ValueError("OpenAI token details must be objects")
        cached, written = count(details, "cached_tokens"), count(details, "cache_write_tokens")
        if cached + written > input_tokens:
            raise ValueError("OpenAI cached/written tokens exceed total input tokens")
        if count(output_details, "reasoning_tokens") > output_tokens:
            raise ValueError("OpenAI reasoning tokens exceed total output tokens")
        if "total_tokens" in usage and count(usage, "total_tokens") != input_tokens + output_tokens:
            raise ValueError("OpenAI total token count disagrees with input/output")
        if cached and self.cache_read_per_million is None:
            raise ValueError("Explicit cached-input pricing is required")
        if written and self.cache_write_per_million is None:
            raise ValueError("Explicit cache-write pricing is required")
        input_cost = (
            (input_tokens - cached - written) * self.input_per_million
            + cached * (self.cache_read_per_million or 0)
            + written * (self.cache_write_per_million or 0)
        )
        output_cost = output_tokens * self.output_per_million
        if input_tokens > self.long_context_threshold_input_tokens:
            input_cost *= self.long_context_input_multiplier
            output_cost *= self.long_context_output_multiplier
        return (input_cost + output_cost) / 1_000_000


class NativeResponseError(FormatError):
    """Terminal protocol failure retained and billed by DefaultAgent.

    DefaultAgent bills FormatError messages before appending them. An exit
    message terminates the loop immediately, avoiding retries for provider/model
    errors. This preserves returned usage even when no command may execute.
    """


class OpenAIResponsesModel:
    """One native bash function call per DefaultAgent turn.

    The requested response model must match exactly, unless the caller supplies
    explicit, preflight-verified snapshot IDs in accepted_response_models. The
    allowlist is recorded; no prefix matching or model substitution occurs here.
    Reasoning effort, context settings, and sampling use provider defaults.
    """

    def __init__(
        self,
        model_name: str,
        *,
        prices: OpenAITokenPrices,
        transport: Callable[[dict], dict],
        max_tokens: int = 8192,
        observation_template: str = DEFAULT_OBSERVATION,
        format_error_template: str = DEFAULT_FORMAT_ERROR,
        accepted_response_models: tuple[str, ...] = (),
    ):
        if not isinstance(model_name, str) or not model_name.strip():
            raise ValueError("A native OpenAI model ID is required")
        if not isinstance(prices, OpenAITokenPrices):
            raise ValueError("Explicit OpenAI token prices are required")
        if not callable(transport):
            raise ValueError("An explicit credential-free transport is required")
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens < 1:
            raise ValueError("max_tokens must be a positive integer")
        if not isinstance(accepted_response_models, (tuple, list)) or any(
            not isinstance(name, str) or not name.strip() for name in accepted_response_models
        ):
            raise ValueError("accepted_response_models must contain explicit model IDs")
        self.model_name = model_name
        self.prices = prices
        self._transport = transport
        self.max_tokens = max_tokens
        self.observation_template = observation_template
        self.format_error_template = format_error_template
        self.accepted_response_models = tuple(dict.fromkeys(accepted_response_models))
        self.config = self.get_template_vars()

    def _payload(self, messages: list[dict]) -> dict:
        history = []
        for message in messages:
            role, content = message.get("role"), deepcopy(message.get("content", ""))
            if role == "assistant" and isinstance(content, list):
                # The full native output is retained, including opaque reasoning.
                history.extend(content)
            elif role == "user" and isinstance(content, list):
                if not all(isinstance(item, dict) and item.get("type") == "function_call_output" for item in content):
                    raise ValueError("Native observation must contain function_call_output items")
                history.extend(content)
            elif role in {"system", "user", "assistant"} and isinstance(content, str):
                # Preserve the rendered original prompt strings byte for byte.
                history.append({"role": role, "content": content})
            else:
                raise ValueError(f"Unexpected native conversation role/content: {role}")
        return {
            "model": self.model_name,
            "input": history,
            "tools": [deepcopy(BASH_TOOL)],
            "tool_choice": "auto",
            "parallel_tool_calls": False,
            "max_output_tokens": self.max_tokens,
            "store": False,
            "include": ["reasoning.encrypted_content"],
        }

    @staticmethod
    def _fatal(message: dict, error: str) -> None:
        raise NativeResponseError(message, {
            "role": "exit", "content": error,
            "extra": {"exit_status": "NativeResponseError", "submission": "", "exception_str": error},
        })

    def query(self, messages: list[dict], **kwargs) -> dict:
        if kwargs:
            raise ValueError("Per-query model overrides are not supported")
        response = self._transport(self._payload(messages))
        if not isinstance(response, dict):
            raise ValueError("Transport must return a decoded native OpenAI response")
        output, usage = response.get("output"), response.get("usage")
        message = {
            "role": "assistant",
            "content": deepcopy(output) if isinstance(output, list) else [],
            "extra": {
                "cost": 0.0, "cost_status": "unknown", "usage": deepcopy(usage),
                "response": deepcopy(response), "timestamp": time.time(),
                "response_created_at": response.get("created_at"),
                "response_completed_at": response.get("completed_at"),
            },
        }
        try:
            message["extra"]["cost"] = self.prices.cost(usage)
            message["extra"]["cost_status"] = "priced"
        except ValueError as error:
            # Zero is only the known billed subtotal, not an assertion that this
            # response was free. Unknown usage is marked and stops the run.
            self._fatal(message, str(error))
        if response.get("model") not in (self.model_name, *self.accepted_response_models):
            message["extra"]["cost_status"] = "requested_model_rate_only"
            self._fatal(message, "OpenAI returned an unexpected model ID; no command was executed.")
        if response.get("object") != "response":
            self._fatal(message, "Transport did not return a native OpenAI response object.")
        if not isinstance(output, list) or not all(isinstance(item, dict) for item in output):
            self._fatal(message, "Native OpenAI output items are malformed.")
        status = response.get("status")
        if status not in ("completed", "incomplete") or response.get("error"):
            self._fatal(message, f"OpenAI response ended with status {status!r}; no command was executed.")

        calls = [item for item in output if item.get("type") == "function_call"]
        error, args = "", None
        if status == "incomplete":
            incomplete_details = response.get("incomplete_details")
            if incomplete_details is not None and not isinstance(incomplete_details, dict):
                self._fatal(message, "Native incomplete response details are malformed.")
            reason = (incomplete_details or {}).get("reason", "unspecified")
            error = (
                "Your previous response hit the output token limit. Be concise and complete one bash tool call."
                if reason == "max_output_tokens" else f"Your previous response was incomplete ({reason}); no command was executed."
            )
        elif any(item.get("type") not in {"function_call", "reasoning", "message"} for item in output):
            error = "Only the bash function tool is available."
        elif len(calls) != 1:
            error = "Exactly one bash tool call is required."
        elif calls[0].get("name") != "bash":
            error = "Only the bash tool is available."
        elif calls[0].get("status") not in (None, "completed"):
            error = "The bash tool call was incomplete; no command was executed."
        else:
            raw_args = calls[0].get("arguments")

            def unique_object(pairs: list[tuple]) -> dict:
                result = {}
                for key, value in pairs:
                    if key in result:
                        raise ValueError("Duplicate JSON argument key")
                    result[key] = value
                return result

            try:
                args = json.loads(raw_args, object_pairs_hook=unique_object) if isinstance(raw_args, str) else None
            except (ValueError, TypeError):
                args = None
            if not isinstance(args, dict) or set(args) != {"command"} or not isinstance(args["command"], str) or not args["command"].strip():
                error = "bash arguments must contain exactly one nonempty string command."
        call_ids = [call.get("call_id") for call in calls]
        if any(not isinstance(call_id, str) or not call_id for call_id in call_ids) or len(set(call_ids)) != len(call_ids):
            self._fatal(message, "Native bash calls have missing or duplicate call IDs and cannot be completed safely.")
        if error:
            correction = Template(self.format_error_template, undefined=StrictUndefined).render(
                error=error, actions=[], has_tool_calls=bool(calls),
                finish_reason="length" if status == "incomplete" else status,
            )
            results = [{"type": "function_call_output", "call_id": call_id, "output": correction} for call_id in call_ids]
            feedback = {"role": "user", "content": results or correction, "extra": {"interrupt_type": "FormatError"}}
            raise FormatError(message, feedback)
        message["extra"]["actions"] = [{"command": args["command"], "tool_call_id": call_ids[0]}]
        return message

    def format_message(self, **kwargs) -> dict:
        return deepcopy(kwargs)

    def format_observation_messages(self, message: dict, outputs: list[dict], template_vars: dict | None = None) -> list[dict]:
        actions = message.get("extra", {}).get("actions", [])
        if len(actions) != 1 or len(outputs) != 1:
            raise ValueError("Exactly one action and observation are required")
        output = outputs[0]
        rendered = Template(self.observation_template, undefined=StrictUndefined).render(output=output, **(template_vars or {}))
        return [{
            "role": "user",
            "content": [{"type": "function_call_output", "call_id": actions[0]["tool_call_id"], "output": rendered}],
            "extra": {
                "raw_output": output.get("output", ""), "returncode": output.get("returncode"), "timestamp": time.time(),
                "exception_info": output.get("exception_info", ""), **deepcopy(output.get("extra", {})),
            },
        }]

    def get_template_vars(self, **kwargs) -> dict[str, Any]:
        return {
            "model_name": self.model_name, "max_tokens": self.max_tokens, "model_kwargs": {},
            "observation_template": self.observation_template, "format_error_template": self.format_error_template,
            "prices": asdict(self.prices), "accepted_response_models": list(self.accepted_response_models),
            "reasoning_policy": "provider_default", "store": False,
        }

    def serialize(self) -> dict:
        return {"info": {"config": {"model": self.get_template_vars(),
                                   "model_type": f"{self.__class__.__module__}.{self.__class__.__name__}"}}}
