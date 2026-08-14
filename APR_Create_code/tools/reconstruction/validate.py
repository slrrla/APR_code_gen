"""Validation and status classification.

Static checks always run; execution runs when the program does not obviously
require remote access. The classifier separates two very different kinds of
runtime failure:

  * the *bug being represented*   -> SUCCESS_WITH_EXPECTED_BUG
  * a *reconstruction defect*     -> NEEDS_REVIEW

A NameError is treated as the latter: it means scaffolding is missing rather
than that the studied defect fired.
"""
from __future__ import annotations

import ast
import difflib
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import config
from .reconstruct import undefined_names

STATUS_SUCCESS = "SUCCESS"
STATUS_EXPECTED_BUG = "SUCCESS_WITH_EXPECTED_BUG"
STATUS_VERSION = "VERSION_INCOMPATIBLE"
STATUS_REVIEW = "NEEDS_REVIEW"
STATUS_FAILED = "GENERATION_FAILED"

#: Exceptions indicating the case targets a Qiskit API absent from the installed
#: version, rather than a reconstruction mistake.
_VERSION_EXCEPTIONS = {"ImportError", "ModuleNotFoundError"}
_VERSION_HINTS = re.compile(
    r"(cannot import name|no module named|has no attribute|is not available|"
    r"was removed|deprecated and removed|qiskit\.aqua|qiskit\.opflow|"
    r"qiskit\.utils|qiskit\.tools|providers\.ibmq|qiskit_aer|qiskit_ibm)",
    re.I,
)

#: Phrases that mark answer/explanation prose leaking into a .py file.
_PROSE_MARKERS = re.compile(
    r"(the problem is|the issue is|you should|you need to|this is because|"
    r"solution:|answer:|try this|hope this helps|the reason is|"
    r"as you can see|in summary|to fix this|the correct way|note that you|"
    r"here'?s how|explanation:|winner:|verdict)",
    re.I,
)


@dataclass
class FileChecks:
    exists: bool = False
    non_empty: bool = False
    syntax_valid: bool = False
    syntax_error: str = ""
    no_fences: bool = True
    no_prose: bool = True
    prose_evidence: str = ""
    line_count: int = 0
    unresolved_names: list[str] = field(default_factory=list)
    oversized: bool = False


@dataclass
class PairChecks:
    identical: bool = False
    similarity: float = 0.0
    structurally_plausible: bool = True


# --------------------------------------------------------------------------
def check_file(path: Path) -> FileChecks:
    c = FileChecks()
    if not path.exists():
        return c
    c.exists = True
    src = path.read_text(encoding="utf-8", errors="replace")
    c.non_empty = bool(src.strip())
    c.line_count = len([ln for ln in src.split("\n") if ln.strip()])
    c.oversized = c.line_count > config.MAX_REASONABLE_LINES
    c.no_fences = "```" not in src and "~~~" not in src

    try:
        tree = ast.parse(src)
        c.syntax_valid = True
    except SyntaxError as exc:
        c.syntax_error = f"line {exc.lineno}: {exc.msg}"
        return c
    except ValueError as exc:
        c.syntax_error = str(exc)[:120]
        return c

    c.no_prose, c.prose_evidence = _check_prose(src, tree)
    c.unresolved_names = undefined_names(src)
    return c


def _check_prose(src: str, tree: ast.AST) -> tuple[bool, str]:
    for ln in src.split("\n"):
        s = ln.strip()
        if not s.startswith("#"):
            continue
        if _PROSE_MARKERS.search(s) and len(s) > 45:
            return False, f"comment prose: {s[:90]}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            text = node.value.value
            if len(text) > 200 and _PROSE_MARKERS.search(text):
                return False, f"string-literal prose: {text[:90]}"
    return True, ""


def check_pair(buggy_src: str, fixed_src: str) -> PairChecks:
    p = PairChecks()
    b, f = buggy_src.strip(), fixed_src.strip()
    p.identical = bool(b) and b == f
    p.similarity = round(difflib.SequenceMatcher(None, b, f).ratio(), 4)
    # A usable APR pair is neither the same program nor two unrelated programs.
    p.structurally_plausible = bool(b) and bool(f) and not p.identical and p.similarity >= 0.05
    return p


# --------------------------------------------------------------------------
def _is_version_failure(exec_result) -> bool:
    if exec_result.status != "ERROR":
        return False
    if exec_result.exc_type in _VERSION_EXCEPTIONS:
        return True
    if exec_result.exc_type == "AttributeError" and _VERSION_HINTS.search(exec_result.stderr_tail):
        return True
    return bool(_VERSION_HINTS.search(exec_result.stderr_tail or ""))


def classify(
    buggy: FileChecks,
    fixed: FileChecks,
    pair: PairChecks,
    buggy_exec,
    fixed_exec,
    question_exists: bool,
    model_needs_review: bool = False,
    model_reason: str = "",
) -> tuple[str, list[str]]:
    """Return (reconstruction_status, notes)."""
    notes: list[str] = []

    # -- generation-level failures ---------------------------------------
    if not buggy.exists or not fixed.exists or not question_exists:
        missing = [n for n, ok in (("buggy.py", buggy.exists), ("fixed.py", fixed.exists),
                                   ("original_question.txt", question_exists)) if not ok]
        return STATUS_FAILED, [f"missing artifact(s): {', '.join(missing)}"]
    if not buggy.non_empty or not fixed.non_empty:
        which = "buggy.py" if not buggy.non_empty else "fixed.py"
        return STATUS_FAILED, [f"{which} has no reconstructable content"]

    # -- reconstruction defects -------------------------------------------
    if not buggy.syntax_valid:
        return STATUS_REVIEW, [f"buggy.py does not parse ({buggy.syntax_error})"]
    if not fixed.syntax_valid:
        return STATUS_REVIEW, [f"fixed.py does not parse ({fixed.syntax_error})"]
    if not buggy.no_fences or not fixed.no_fences:
        return STATUS_REVIEW, ["markdown fence survived cleaning"]
    if not buggy.no_prose:
        return STATUS_REVIEW, [f"prose contamination in buggy.py ({buggy.prose_evidence})"]
    if not fixed.no_prose:
        return STATUS_REVIEW, [f"prose contamination in fixed.py ({fixed.prose_evidence})"]
    if pair.identical:
        return STATUS_REVIEW, ["buggy.py and fixed.py are identical; not a usable APR pair"]
    if not pair.structurally_plausible:
        return STATUS_REVIEW, [f"pair not structurally plausible (similarity {pair.similarity})"]

    # -- the model's own conservatism flag ---------------------------------
    if model_needs_review:
        return STATUS_REVIEW, [
            f"flagged during reconstruction: {model_reason or 'source too incomplete to reconstruct faithfully'}"
        ]

    if buggy.oversized or fixed.oversized:
        notes.append(
            f"unusually large program (buggy {buggy.line_count} / fixed {fixed.line_count} lines)"
        )

    # -- version incompatibility -------------------------------------------
    if _is_version_failure(fixed_exec) or _is_version_failure(buggy_exec):
        who = "fixed" if _is_version_failure(fixed_exec) else "buggy"
        exc = fixed_exec if who == "fixed" else buggy_exec
        notes.append(f"{who}.py needs an API absent from the installed Qiskit ({exc.exc_type})")
        return STATUS_VERSION, notes

    # -- scaffolding defects surfaced at runtime ----------------------------
    if buggy_exec.status == "ERROR" and buggy_exec.exc_type == "NameError":
        return STATUS_REVIEW, notes + [
            "buggy.py raised NameError: scaffolding is incomplete, not a represented bug"
        ]
    if fixed_exec.status == "ERROR" and fixed_exec.exc_type == "NameError":
        return STATUS_REVIEW, notes + ["fixed.py raised NameError: scaffolding is incomplete"]

    if buggy.unresolved_names:
        notes.append(f"unresolved names in buggy.py: {', '.join(buggy.unresolved_names[:6])}")
    if fixed.unresolved_names:
        notes.append(f"unresolved names in fixed.py: {', '.join(fixed.unresolved_names[:6])}")

    # -- execution-informed outcomes ----------------------------------------
    if fixed_exec.status == "TIMEOUT":
        return STATUS_REVIEW, notes + ["fixed.py exceeded the execution timeout"]
    if fixed_exec.status == "ERROR":
        return STATUS_REVIEW, notes + [
            f"fixed.py failed at runtime ({fixed_exec.exc_type}); a fix is expected to run"
        ]
    if fixed_exec.status in ("SKIPPED_NETWORK", "SKIPPED_DISABLED", "NOT_RUN"):
        notes.append("not executed (remote access required or execution disabled); "
                     "validated statically only")
        return STATUS_SUCCESS, notes

    if fixed_exec.status == "OK":
        if buggy_exec.status == "ERROR":
            notes.append(f"buggy.py fails with {buggy_exec.exc_type}, consistent with the case")
            return STATUS_EXPECTED_BUG, notes
        if buggy_exec.status == "TIMEOUT":
            notes.append("buggy.py timed out; may represent a hang-type defect")
            return STATUS_EXPECTED_BUG, notes
        if buggy_exec.status in ("SKIPPED_NETWORK", "SKIPPED_DISABLED", "NOT_RUN"):
            notes.append("buggy.py not executed (remote access required)")
            return STATUS_SUCCESS, notes
        return STATUS_SUCCESS, notes + ["both programs run; defect is semantic rather than fatal"]

    return STATUS_REVIEW, notes + [f"unclassified execution outcome ({fixed_exec.summary})"]
