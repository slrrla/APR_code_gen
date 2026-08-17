"""LLM layer: prompt construction, provider abstraction, response parsing.

Semantic reconstruction happens here. The deterministic pipeline decides *what*
to send and *how to check* what comes back; the model decides what the program
actually was.

Providers
---------
``anthropic``  real calls, needs ANTHROPIC_API_KEY.
``stub``       offline. Runs the static cleaner so the plumbing (prompting,
               caching, validation, execution, reporting) can be exercised
               end-to-end without credentials. Stub output is tagged in the
               report and must never be presented as model-reconstructed data.
"""
from __future__ import annotations

import os
import random
import re
import time
from dataclasses import dataclass, field

from . import config, preprocess
from .loader import CaseView


class LLMUnavailable(RuntimeError):
    """No usable LLM credential/provider."""


@dataclass
class LLMResponse:
    text: str
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    provider: str = ""


# --------------------------------------------------------------------------
# Prompt
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You reconstruct ground-truth bug/fix program pairs for an Automated Program \
Repair dataset built from Qiskit questions on Stack Exchange and Stack Overflow.

You are given one case: a title, a category, the asker's question, the buggy \
code as scraped, the answer's explanation, and the fixed code as scraped. Reason \
over ALL of it jointly. The fix tells you what the question was really about; \
the question tells you what the fix is correcting. Use each to fill gaps in the \
other.

The scraped code is damaged. Expect: newlines stripped so statements run \
together on one physical line, blocks concatenated, prose mixed into code \
fields, fragments that are only a symbol name, and truncation. Your job is to \
recover the program the author actually ran.

Produce exactly two Python programs.

buggy.py
  * A minimal, self-contained program that reproduces the reported problem.
  * PRESERVE THE BUG. Never repair it. If the reported failure is a missing or \
wrong import, the missing/wrong import must remain missing/wrong.
  * Add only the scaffolding needed to reach the buggy behaviour: imports the \
author clearly had, circuit setup, variable definitions.

fixed.py
  * The same conceptual task with the reported correction applied.
  * Change only what the fix requires. Keep structure, names and ordering \
aligned with buggy.py so the diff isolates the repair.

Both files
  * Valid Python. No markdown fences. No prose, no explanation text, no \
commentary about the answer. Comments only where they are ordinary code comments.
  * As small as practical while still executable.
  * PRESERVE THE QISKIT ERA of the source case. If the case is from Qiskit 0.x \
(execute(), Aer from qiskit, IBMQ, QuantumInstance, aqua, opflow), keep that API. \
Do NOT modernise it; a version mismatch is recorded separately and is not your \
problem to solve. Equally, do not backport a modern case.
  * Never contact a real backend. No IBM Quantum credentials, no network calls. \
Prefer local simulators. If the original used a hardware backend, use the \
closest local simulator and keep everything else identical.
  * Do not fabricate datasets, expected outputs, fake results or unrelated \
algorithms. Simple deterministic placeholder values are fine when a value is \
missing and is needed to run, provided the placeholder does not change the bug.

If the source material is too incomplete or ambiguous to reconstruct \
faithfully, do NOT invent an elaborate program. Produce the most conservative \
reconstruction the evidence supports and set needs_review: true with a short \
reason. Research validity matters more than a program that merely looks complete.

Respond in exactly this format and nothing else:

<BUGGY_PY>
(python source)
</BUGGY_PY>
<FIXED_PY>
(python source)
</FIXED_PY>
<META>
needs_review: true|false
api_era: legacy|modern|unknown
bug_summary: one line describing the defect
fix_summary: one line describing the correction
reason: short note, required when needs_review is true
</META>
"""


def build_prompt(view: CaseView) -> tuple[str, list[str]]:
    """Assemble the user message from the full row. Returns (prompt, observations)."""
    b = config.FIELD_CHAR_BUDGET
    obs: list[str] = []

    title, _ = preprocess.truncate(view.title, b["title"])
    cat = view.category_label[: b["category_label"]] or "(none recorded)"

    q, o = preprocess.render_prose(
        view.buggy_question_description, "QUESTION", b["buggy_question_description"])
    obs += o
    bc, o = preprocess.render_cell(view.buggy_code, "BUGGY CODE", b["buggy_code"])
    obs += o
    ex, o = preprocess.render_prose(
        view.fixed_solution_explanation, "SOLUTION EXPLANATION", b["fixed_solution_explanation"])
    obs += o
    fc, o = preprocess.render_cell(view.fixed_code, "FIXED CODE", b["fixed_code"])
    obs += o

    notes = ""
    if obs:
        notes = ("\nKnown damage in this row (detected automatically):\n"
                 + "\n".join(f"  - {o}" for o in dict.fromkeys(obs)) + "\n")

    prompt = f"""\
CASE {view.case_id}  (platform={view.platform}, issue_id={view.issue_id})

TITLE: {title}
CATEGORY: {cat}
{notes}
{q}

{bc}

{ex}

{fc}

Reconstruct buggy.py and fixed.py for this case."""
    return prompt, obs


# --------------------------------------------------------------------------
# Response parsing
# --------------------------------------------------------------------------
@dataclass
class ParsedPair:
    buggy: str = ""
    fixed: str = ""
    needs_review: bool = False
    api_era: str = "unknown"
    bug_summary: str = ""
    fix_summary: str = ""
    reason: str = ""
    parse_error: str = ""


_BLOCK = {
    "buggy": re.compile(r"<BUGGY_PY>\s*\n?(.*?)</BUGGY_PY>", re.S | re.I),
    "fixed": re.compile(r"<FIXED_PY>\s*\n?(.*?)</FIXED_PY>", re.S | re.I),
    "meta": re.compile(r"<META>\s*\n?(.*?)</META>", re.S | re.I),
}
_FENCE = re.compile(r"^\s*(?:```|~~~)[a-zA-Z0-9_+-]*\s*\n(.*?)\n\s*(?:```|~~~)\s*$", re.S)


def _strip_fence(code: str) -> str:
    """The model is told not to fence; strip one anyway if it slips through."""
    m = _FENCE.match(code.strip())
    return m.group(1) if m else code


def parse_response(text: str) -> ParsedPair:
    p = ParsedPair()
    mb, mf = _BLOCK["buggy"].search(text), _BLOCK["fixed"].search(text)
    if not mb or not mf:
        p.parse_error = "response did not contain both <BUGGY_PY> and <FIXED_PY> blocks"
        return p
    p.buggy = _strip_fence(mb.group(1)).strip("\n")
    p.fixed = _strip_fence(mf.group(1)).strip("\n")

    mm = _BLOCK["meta"].search(text)
    if mm:
        for line in mm.group(1).splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip().lower(), v.strip()
            if k == "needs_review":
                p.needs_review = v.lower().startswith("t") or v.lower() == "yes"
            elif k == "api_era" and v.lower() in ("legacy", "modern", "unknown"):
                p.api_era = v.lower()
            elif k == "bug_summary":
                p.bug_summary = v[:200]
            elif k == "fix_summary":
                p.fix_summary = v[:200]
            elif k == "reason":
                p.reason = v[:300]
    return p


REPAIR_TEMPLATE = """\
The {which} program you produced for this case does not parse as Python:

{error}

Here is what you produced:

{source}

Return the corrected pair in the same <BUGGY_PY>/<FIXED_PY>/<META> format. Fix \
only the syntax problem. Do not change the semantics, and in particular do not \
repair the bug in buggy.py."""


# --------------------------------------------------------------------------
# Providers
# --------------------------------------------------------------------------
class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model: str | None = None):
        key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
        if not key:
            raise LLMUnavailable(
                "ANTHROPIC_API_KEY is not set. Export a key, or run with "
                "--provider stub for an offline plumbing test."
            )
        try:
            import anthropic
        except ImportError as exc:
            raise LLMUnavailable("the 'anthropic' package is not installed") from exc
        self.model = model or config.LLM_MODEL
        self._client = anthropic.Anthropic(
            api_key=key,
            base_url=os.environ.get("ANTHROPIC_BASE_URL") or None,
            timeout=config.LLM_TIMEOUT_S,
            max_retries=0,  # retry policy is ours, below
        )

    def complete(self, system: str, user: str) -> LLMResponse:
        import anthropic

        last: Exception | None = None
        for attempt in range(config.LLM_MAX_RETRIES):
            try:
                kwargs = dict(
                    model=self.model,
                    max_tokens=config.LLM_MAX_TOKENS,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                # Newer models reject an explicit temperature; only send one
                # when the config asks for it.
                if config.LLM_TEMPERATURE is not None:
                    kwargs["temperature"] = config.LLM_TEMPERATURE
                msg = self._client.messages.create(**kwargs)
                text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
                return LLMResponse(
                    text=text,
                    model=self.model,
                    input_tokens=getattr(msg.usage, "input_tokens", 0),
                    output_tokens=getattr(msg.usage, "output_tokens", 0),
                    provider=self.name,
                )
            except (anthropic.RateLimitError, anthropic.APIStatusError,
                    anthropic.APIConnectionError) as exc:
                last = exc
                status = getattr(exc, "status_code", None)
                if status in (400, 401, 403, 404):
                    raise  # not transient
                delay = config.LLM_RETRY_BASE_DELAY * (2 ** attempt)
                time.sleep(delay + random.uniform(0, 0.5))
        raise RuntimeError(f"LLM call failed after {config.LLM_MAX_RETRIES} attempts: {last}")


class StubProvider:
    """Offline provider. Static cleaning only; NOT a semantic reconstruction.

    Exists so the surrounding pipeline can be validated without credentials.
    Anything it produces is tagged provider=stub in the report.
    """

    name = "stub"

    def __init__(self, model: str | None = None):
        self.model = "stub"

    def complete(self, system: str, user: str) -> LLMResponse:
        from . import stubgen
        return LLMResponse(text=stubgen.generate(user), model="stub", provider=self.name)


def get_provider(name: str | None = None, model: str | None = None):
    name = (name or config.LLM_PROVIDER).lower()
    if name == "anthropic":
        return AnthropicProvider(model)
    if name == "stub":
        return StubProvider(model)
    raise LLMUnavailable(f"unknown provider {name!r}")
