"""Status and pair classification for the execution matrix.

The distinction that decides whether this experiment means anything:

    VERSION_INCOMPATIBLE  the case needs a Qiskit API this release does not
                          have. That is a real historical finding.
    ENVIRONMENT_ERROR     we failed to provide something the program needs
                          (a third-party package, a working interpreter).
                          That is our problem and must never be reported as a
                          Qiskit incompatibility.

They are told apart by *which* module the import failure names: a
qiskit-family module means the former, anything else means the latter.
"""
from __future__ import annotations

import re

from . import config

# -- per-program statuses ---------------------------------------------------
PASS = "PASS"
FAIL = "FAIL"
TIMEOUT = "TIMEOUT"
ENVIRONMENT_ERROR = "ENVIRONMENT_ERROR"
VERSION_INCOMPATIBLE = "VERSION_INCOMPATIBLE"
NOT_TESTABLE = "NOT_TESTABLE"

SHORT = {
    PASS: "P", FAIL: "F", TIMEOUT: "T",
    ENVIRONMENT_ERROR: "E", VERSION_INCOMPATIBLE: "V", NOT_TESTABLE: "N",
}

# -- pair classifications ---------------------------------------------------
VALID_REPAIR = "VALID_REPAIR"
BUG_NOT_REPRODUCED = "BUG_NOT_REPRODUCED"
FIX_NOT_WORKING = "FIX_NOT_WORKING"
REGRESSION = "REGRESSION"
NOT_EVALUABLE = "NOT_EVALUABLE"

_MISSING_MODULE = re.compile(
    r"(?:ModuleNotFoundError|ImportError):.*?(?:No module named|cannot import name)\s+['\"]?([\w.]+)",
    re.I)
_IMPORT_FROM = re.compile(r"cannot import name ['\"]([\w.]+)['\"] from ['\"]([\w.]+)['\"]", re.I)
_ATTR_ERR = re.compile(r"AttributeError:.*?'([\w.]+)'", re.I)
_QISKIT_MENTION = re.compile(r"\bqiskit[\w.]*", re.I)


def _root(mod: str) -> str:
    return (mod or "").split(".")[0]


def _is_qiskit_family(mod: str) -> bool:
    return _root(mod).lower() in {m.lower() for m in config.QISKIT_FAMILY}


def _is_known_third_party(mod: str) -> bool:
    r = _root(mod).lower()
    return any(r == h.lower() or r.startswith(h.lower()) for h in config.THIRD_PARTY_HINTS)


def classify_program(
    exit_code: int | None,
    stderr: str,
    timed_out: bool,
    env_ok: bool,
    wants_network: bool,
    launch_error: str = "",
) -> tuple[str, str]:
    """Return (status, reason)."""
    if not env_ok:
        return ENVIRONMENT_ERROR, "environment for this Qiskit version was not built"
    if wants_network:
        return NOT_TESTABLE, "program requires IBM Quantum access; not executed locally"
    if launch_error:
        return ENVIRONMENT_ERROR, f"could not launch interpreter: {launch_error[:200]}"
    if timed_out:
        return TIMEOUT, f"exceeded {config.EXEC_TIMEOUT_SECONDS}s"
    if exit_code == 0:
        return PASS, ""

    err = stderr or ""

    # cannot-import-name gives both the symbol and its module; the module decides.
    m = _IMPORT_FROM.search(err)
    if m:
        symbol, module = m.group(1), m.group(2)
        if _is_qiskit_family(module):
            return VERSION_INCOMPATIBLE, f"{module} has no {symbol} in this release"
        if _is_known_third_party(module):
            return ENVIRONMENT_ERROR, f"third-party module {module} lacks {symbol}"

    m = _MISSING_MODULE.search(err)
    if m:
        mod = m.group(1)
        if _is_qiskit_family(mod):
            return VERSION_INCOMPATIBLE, f"{mod} not available in this release"
        return ENVIRONMENT_ERROR, f"missing dependency {mod} in our environment"

    # AttributeError on a qiskit object is an API-shape change.
    if "AttributeError" in err and _QISKIT_MENTION.search(err):
        m = _ATTR_ERR.search(err)
        detail = m.group(1) if m else "qiskit object"
        return VERSION_INCOMPATIBLE, f"AttributeError on {detail}; API differs in this release"

    if "TypeError" in err and _QISKIT_MENTION.search(err) and (
            "unexpected keyword argument" in err or "positional argument" in err):
        return VERSION_INCOMPATIBLE, "qiskit call signature differs in this release"

    return FAIL, "program ran and failed"


# --------------------------------------------------------------------------
_BLOCKING = {TIMEOUT, ENVIRONMENT_ERROR, VERSION_INCOMPATIBLE, NOT_TESTABLE}


def classify_pair(buggy_status: str, fixed_status: str) -> str:
    if buggy_status in _BLOCKING or fixed_status in _BLOCKING:
        return NOT_EVALUABLE
    if buggy_status == FAIL and fixed_status == PASS:
        return VALID_REPAIR
    if buggy_status == PASS and fixed_status == PASS:
        return BUG_NOT_REPRODUCED
    if buggy_status == FAIL and fixed_status == FAIL:
        return FIX_NOT_WORKING
    if buggy_status == PASS and fixed_status == FAIL:
        return REGRESSION
    return NOT_EVALUABLE


# --------------------------------------------------------------------------
def evaluate_behaviour(oracle: dict | None, buggy_stdout: str, fixed_stdout: str,
                       buggy_status: str, fixed_status: str) -> tuple[str, str, str]:
    """Compare observable output against an inferred oracle.

    Returns (behavioral_bug_reproduced, behavioral_fix_verified, evidence),
    each of the first two being "YES" / "NO" / "UNKNOWN". UNKNOWN is the honest
    answer whenever no oracle could be inferred confidently, and is never
    upgraded by guessing.
    """
    if not oracle or oracle.get("oracle") != "yes":
        return "UNKNOWN", "UNKNOWN", "no behavioral oracle could be inferred from the source"
    if fixed_status != PASS:
        return "UNKNOWN", "NO", "fixed.py did not run, so its behaviour cannot be checked"

    fixed_expect = [str(s) for s in oracle.get("fixed_expected_substrings", []) if str(s).strip()]
    buggy_expect = [str(s) for s in oracle.get("buggy_expected_substrings", []) if str(s).strip()]
    if not fixed_expect:
        return "UNKNOWN", "UNKNOWN", "oracle carried no expected output for fixed.py"

    fout = fixed_stdout or ""
    bout = buggy_stdout or ""

    fix_ok = all(s in fout for s in fixed_expect)
    fix_verdict = "YES" if fix_ok else "NO"
    evidence = f"fixed.py expected {fixed_expect!r}; got {fout.strip()[:160]!r}"

    if buggy_status != PASS:
        return "UNKNOWN", fix_verdict, evidence + " | buggy.py did not run to completion"

    if buggy_expect:
        bug_ok = all(s in bout for s in buggy_expect) and bout.strip() != fout.strip()
        bug_verdict = "YES" if bug_ok else "NO"
        evidence += f" | buggy.py expected {buggy_expect!r}; got {bout.strip()[:160]!r}"
    else:
        # No positive expectation for the buggy side: the defect is confirmed
        # when the buggy output differs and misses what the fix must produce.
        differs = bout.strip() != fout.strip()
        bug_ok = differs and not all(s in bout for s in fixed_expect)
        bug_verdict = "YES" if bug_ok else "NO"
        evidence += f" | buggy.py produced {bout.strip()[:160]!r} (differs={differs})"

    return bug_verdict, fix_verdict, evidence


def ground_truth_confirmed(pair_class: str, behav_bug: str, behav_fix: str) -> bool:
    """A) buggy fails as expected and fixed passes, or
       B) both run but the buggy behaviour is demonstrably wrong."""
    if pair_class == VALID_REPAIR:
        return True
    return behav_bug == "YES" and behav_fix == "YES"
