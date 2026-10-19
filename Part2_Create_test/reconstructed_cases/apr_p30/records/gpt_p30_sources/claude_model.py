"""Native Anthropic Messages model for mini-swe-agent's DefaultAgent.

``transport(payload: dict) -> dict`` receives the complete Messages request body
and returns the decoded native response. Supplying it requires no API key and
never invokes HTTP here; this supports a separate credential-bearing broker.
Assistant content blocks are retained unchanged, including thinking signatures.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import json
import math
import os
import time
from typing import Any, Callable
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from jinja2 import StrictUndefined, Template
from minisweagent.exceptions import FormatError


BASH_TOOL = {
    "name": "bash",
    "description": "Execute one bash command in the repair workspace.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
        "additionalProperties": False,
    },
}

DEFAULT_OBSERVATION = (
    "<returncode>{{ output.returncode }}</returncode>\n"
    "<output>{{ output.output }}</output>\n"
    "{% if output.exception_info %}<exception>{{ output.exception_info }}</exception>{% endif %}"
)
DEFAULT_FORMAT_ERROR = (
    "{{ error }} Every response must include exactly one bash tool call with "
    '{"command": "..."}. To finish, run '
    "`echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT` on its own."
)


@dataclass(frozen=True)
class TokenPrices:
    """Explicit USD prices per million tokens; no inferred model pricing."""

    input_per_million: float
    output_per_million: float
    cache_write_per_million: float
    cache_read_per_million: float
    cache_write_1h_per_million: float | None = None

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if name == "cache_write_1h_per_million" and value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"Invalid token price: {name}")

    def cost(self, usage: dict) -> float:
        def count(key: str, data: dict = usage) -> int:
            value = data.get(key, 0)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"Invalid Anthropic usage count: {key}")
            return value

        if "input_tokens" not in usage or "output_tokens" not in usage:
            raise ValueError("Anthropic response is missing input/output usage")
        creation = count("cache_creation_input_tokens")
        detail = usage.get("cache_creation")
        write_cost = creation * self.cache_write_per_million
        if detail is not None:
            if not isinstance(detail, dict):
                raise ValueError("Invalid Anthropic cache creation usage")
            five_min = count("ephemeral_5m_input_tokens", detail)
            one_hour = count("ephemeral_1h_input_tokens", detail)
            if five_min + one_hour != creation:
                raise ValueError("Anthropic cache creation counts disagree")
            if one_hour and self.cache_write_1h_per_million is None:
                raise ValueError("Explicit one-hour cache pricing is required")
            write_cost = five_min * self.cache_write_per_million + one_hour * (self.cache_write_1h_per_million or 0)
        return (
            count("input_tokens") * self.input_per_million
            + count("output_tokens") * self.output_per_million
            + count("cache_read_input_tokens") * self.cache_read_per_million
            + write_cost
        ) / 1_000_000


class AnthropicMessagesModel:
    """DefaultAgent-compatible model using one native bash call per turn.

    No cache markers are added. The custom transport owns authentication,
    retries, and network policy; the default transport performs one HTTP call.
    """

    def __init__(
        self,
        model_name: str,
        *,
        prices: TokenPrices,
        api_key: str | None = None,
        max_tokens: int = 8192,
        timeout: float = 120,
        observation_template: str = DEFAULT_OBSERVATION,
        format_error_template: str = DEFAULT_FORMAT_ERROR,
        model_kwargs: dict | None = None,
        transport: Callable[[dict], dict] | None = None,
    ):
        if not model_name or not isinstance(model_name, str):
            raise ValueError("A native Anthropic model ID is required")
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens < 1:
            raise ValueError("max_tokens must be a positive integer")
        if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be positive and finite")
        allowed_kwargs = {"temperature", "top_p", "top_k", "thinking", "output_config", "metadata", "stop_sequences"}
        self.model_kwargs = deepcopy(model_kwargs or {})
        unsupported = set(self.model_kwargs) - allowed_kwargs
        if unsupported:
            raise ValueError("Unsupported native model arguments: " + ", ".join(sorted(unsupported)))
        self.model_name = model_name
        self.prices = prices
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.observation_template = observation_template
        self.format_error_template = format_error_template
        # A broker transport must not need, load, or retain a worker-side key.
        self._api_key = (api_key or os.getenv("ANTHROPIC_API_KEY")) if transport is None else None
        if transport is None and not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY or an explicit transport is required")
        self._transport = transport or self._post
        self.config = self.get_template_vars()

    def _post(self, payload: dict) -> dict:
        request = Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"content-type": "application/json", "anthropic-version": "2023-06-01", "x-api-key": self._api_key},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as error:
            # Do not expose request headers or credentials in trajectories.
            try:
                detail = json.loads(error.read()).get("error", {})
                kind = detail.get("type", "unknown_error")
                message = detail.get("message", "Anthropic request failed")
            except (ValueError, AttributeError):
                kind, message = "unknown_error", "Anthropic request failed"
            if self._api_key:
                message = str(message).replace(self._api_key, "[redacted]")
            raise RuntimeError(f"Anthropic HTTP {error.code}: {kind}: {message}") from None

    def _payload(self, messages: list[dict]) -> dict:
        system = []
        history = []
        for message in messages:
            role, content = message.get("role"), deepcopy(message.get("content", ""))
            if role == "system":
                system.extend(content if isinstance(content, list) else [{"type": "text", "text": content}])
            elif role in {"user", "assistant"}:
                history.append({"role": role, "content": content})
            else:
                raise ValueError(f"Unexpected native conversation role: {role}")
        payload = {
            "model": self.model_name,
            "max_tokens": self.max_tokens,
            "tools": [deepcopy(BASH_TOOL)],
            "tool_choice": {"type": "auto", "disable_parallel_tool_use": True},
            "messages": history,
            **deepcopy(self.model_kwargs),
        }
        if system:
            payload["system"] = system
        return payload

    def query(self, messages: list[dict], **kwargs) -> dict:
        if kwargs:
            raise ValueError("Per-query model overrides are not supported")
        response = self._transport(self._payload(messages))
        if not isinstance(response, dict) or response.get("type") != "message" or response.get("role") != "assistant":
            raise ValueError("Transport must return a native Anthropic assistant message")
        content = response.get("content")
        usage = response.get("usage")
        if not isinstance(content, list) or not all(isinstance(block, dict) for block in content) or not isinstance(usage, dict):
            raise ValueError("Native response content or usage is malformed")
        cost = self.prices.cost(usage)
        message = {
            "role": "assistant",
            "content": deepcopy(content),
            "extra": {"cost": cost, "usage": deepcopy(usage), "response": deepcopy(response), "timestamp": time.time()},
        }
        tools = [block for block in content if block.get("type") == "tool_use"]
        error = ""
        if response.get("stop_reason") == "max_tokens":
            error = "Your previous response hit the output token limit. Be concise and complete one bash tool call."
        elif len(tools) != 1:
            error = "Exactly one bash tool call is required."
        elif tools[0].get("name") != "bash":
            error = "Only the bash tool is available."
        else:
            args = tools[0].get("input")
            if not isinstance(args, dict) or set(args) != {"command"} or not isinstance(args["command"], str) or not args["command"].strip():
                error = "bash input must contain exactly one nonempty string command."
            elif not isinstance(tools[0].get("id"), str) or not tools[0]["id"]:
                error = "bash tool call is missing its native ID."
        if error:
            correction = Template(self.format_error_template, undefined=StrictUndefined).render(
                error=error,
                actions=[],
                has_tool_calls=bool(tools),
                finish_reason="length" if response.get("stop_reason") == "max_tokens" else response.get("stop_reason"),
            )
            # A malformed turn remains in the trajectory and must be billed.
            # Reply to every complete tool ID without executing any command.
            results = [
                {"type": "tool_result", "tool_use_id": block["id"], "content": correction, "is_error": True}
                for block in tools if isinstance(block.get("id"), str) and block["id"]
            ]
            feedback = {"role": "user", "content": results or correction, "extra": {"interrupt_type": "FormatError"}}
            raise FormatError(message, feedback)
        message["extra"]["actions"] = [{"command": tools[0]["input"]["command"], "tool_call_id": tools[0]["id"]}]
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
            "content": [{"type": "tool_result", "tool_use_id": actions[0]["tool_call_id"], "content": rendered}],
            "extra": {"raw_output": output.get("output", ""), "returncode": output.get("returncode"), "timestamp": time.time(),
                      "exception_info": output.get("exception_info", ""), **deepcopy(output.get("extra", {}))},
        }]

    def get_template_vars(self, **kwargs) -> dict[str, Any]:
        return {"model_name": self.model_name, "max_tokens": self.max_tokens, "model_kwargs": deepcopy(self.model_kwargs),
                "observation_template": self.observation_template, "format_error_template": self.format_error_template,
                "prices": asdict(self.prices), "timeout": self.timeout}

    def serialize(self) -> dict:
        return {"info": {"config": {"model": self.get_template_vars(),
                                   "model_type": f"{self.__class__.__module__}.{self.__class__.__name__}"}}}
