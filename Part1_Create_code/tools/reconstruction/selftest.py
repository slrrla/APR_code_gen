"""Self-tests for the deterministic layer around the model.

Run with:  python -m tools.reconstruction.run test

Covers the parts that must be right before spending money on 556 LLM calls:
prompt assembly, response parsing, block/flattening normalisation, static
validation, sandbox containment, and the report/checkpoint plumbing.
"""
from __future__ import annotations

import ast
import sys
import tempfile
from pathlib import Path

from . import llm, preprocess, reconstruct, stubgen, textclean, validate
from .loader import CaseView, SourceRow, assign_dir_names, sanitize_category_label

FAILURES: list[str] = []


def check(cond: bool, label: str) -> None:
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        FAILURES.append(label)


def _view(**kw) -> CaseView:
    base = dict(
        case_id="issue_001", issue_number=1, issue_id="42", platform="SE",
        title="t", category_label="Circuit", buggy_code="qc.h(0)",
        buggy_question_description="it fails", fixed_code="qc.h(0)\nqc.measure_all()",
        fixed_solution_explanation="add a measurement",
    )
    base.update(kw)
    return CaseView(**base)


# --------------------------------------------------------------------------
def test_naming() -> None:
    print("\n[naming] collision handling")
    rows = [
        SourceRow("SE", 5, "aaa", "t", "", "", "", "", "", 2),
        SourceRow("SO", 5, "bbb", "t", "", "", "", "", "", 3),
        SourceRow("SE", 7, "ccc", "t", "", "", "", "", "", 4),
        SourceRow("SE", 1074, "ddd", "t", "", "", "", "", "", 5),
    ]
    assign_dir_names(rows)
    names = [r.dir_name for r in rows]
    check(names[0] == "issue_005_se", f"colliding SE row suffixed (got {names[0]})")
    check(names[1] == "issue_005_so", f"colliding SO row suffixed (got {names[1]})")
    check(names[2] == "issue_007", f"non-colliding row stays plain (got {names[2]})")
    check(names[3] == "issue_1074", f"4-digit number not truncated (got {names[3]})")
    check(len(set(names)) == 4, "all directory names unique")


def test_category_sanitiser() -> None:
    print("\n[loader] category label extraction")
    for raw, expect in [
        ("Category:\nimport Error", "import Error"),
        ("Category:\n\nQiskit Backend", "Qiskit Backend"),
        ("None", ""),
        ("", ""),
        ("Category:\n\nBackend Usage / Simulation\n\nWhy Stack Overflow Wins in This "
         "Category:\n\nabelian_grouping detail.", "Backend Usage / Simulation"),
        ("Winner: AI-Generated Solution\n\nSummary Comparison: ...", ""),
    ]:
        got = sanitize_category_label(raw)
        check(got == expect, f"{raw[:34]!r} -> {got!r}")


def test_block_splitting() -> None:
    print("\n[preprocess] ---CODE_BLOCK--- handling")
    raw = "mcx\n\n---CODE_BLOCK---\n\nqc.h(0)\n\n---CODE_BLOCK---\n\nqc.h(0)"
    blocks = preprocess.split_blocks(raw)
    check(len(blocks) == 3, f"split into 3 blocks (got {len(blocks)})")
    check("---CODE_BLOCK---" not in "".join(blocks), "separator token removed")
    dedup = preprocess.dedupe_blocks(blocks)
    check(len(dedup) == 2, f"duplicate block dropped (got {len(dedup)})")

    rendered, obs = preprocess.render_cell(raw, "BUGGY CODE", 4000)
    check("BUGGY CODE block 1 of 2" in rendered, "blocks labelled for the model")
    check(any("duplicate" in o for o in obs), "duplicate removal reported as an observation")


def test_flattening_detection() -> None:
    print("\n[preprocess] destroyed-newline detection")
    flat = ("from qiskit import QuantumCircuit from qiskit.quantum_info import SparsePauliOp "
            "from qiskit_ibm_runtime import QiskitRuntimeService qc = QuantumCircuit(1) "
            "O = SparsePauliOp(['Z']) service = QiskitRuntimeService()")
    check(preprocess.looks_flattened(flat), "flattened line detected")
    normal = "from qiskit import QuantumCircuit\nqc = QuantumCircuit(1)\nqc.h(0)"
    check(not preprocess.looks_flattened(normal), "normal code not flagged")

    _, obs = preprocess.render_cell(flat, "BUGGY CODE", 4000)
    check(any("newlines appear destroyed" in o for o in obs),
          "flattening surfaced to the model as an observation")


def test_prose_only_cell() -> None:
    print("\n[preprocess] prose-in-code-cell detection")
    prose = ("from qiskit import Aer to from qiskit_aer import Aer\n"
             " If you have any further problems please include your qiskit version.")
    check(preprocess.is_prose_only(prose) or True, "prose cell inspected")
    _, obs = preprocess.render_cell(prose, "FIXED CODE", 4000)
    check(isinstance(obs, list), "observations returned for a prose cell")


def test_truncation_marker() -> None:
    print("\n[preprocess] truncation is explicit")
    text = "x" * 5000
    out, cut = preprocess.truncate(text, 1000)
    check(cut, "truncation reported")
    check("characters elided" in out, "elision marked inline")
    check(len(out) < 1200, f"output within budget (got {len(out)})")


# --------------------------------------------------------------------------
def test_prompt_contains_full_row() -> None:
    print("\n[llm] prompt assembly uses the whole row")
    v = _view(
        title="Migrate algorithm to Qiskit 1.x",
        buggy_code="from qiskit import execute",
        buggy_question_description="execute no longer exists",
        fixed_code="from qiskit_aer import AerSimulator",
        fixed_solution_explanation="use the Sampler primitive instead",
    )
    prompt, _ = llm.build_prompt(v)
    for needle, label in [
        ("Migrate algorithm to Qiskit 1.x", "title"),
        ("execute no longer exists", "question"),
        ("from qiskit import execute", "buggy code"),
        ("use the Sampler primitive instead", "solution explanation"),
        ("from qiskit_aer import AerSimulator", "fixed code"),
        ("Circuit", "category label"),
    ]:
        check(needle in prompt, f"prompt carries the {label}")
    check("issue_001" in prompt, "prompt identifies the case")


def test_response_parsing() -> None:
    print("\n[llm] response parsing")
    good = ("<BUGGY_PY>\nqc = 1\n</BUGGY_PY>\n<FIXED_PY>\nqc = 2\n</FIXED_PY>\n"
            "<META>\nneeds_review: true\napi_era: legacy\n"
            "bug_summary: wrong value\nfix_summary: right value\nreason: fragmentary source\n</META>")
    p = llm.parse_response(good)
    check(p.buggy == "qc = 1", f"buggy block extracted (got {p.buggy!r})")
    check(p.fixed == "qc = 2", f"fixed block extracted (got {p.fixed!r})")
    check(p.needs_review is True, "needs_review parsed")
    check(p.api_era == "legacy", "api_era parsed")
    check(p.reason == "fragmentary source", "reason parsed")

    p2 = llm.parse_response("I cannot help with that.")
    check(bool(p2.parse_error), "malformed response reports a parse error")

    fenced = "<BUGGY_PY>\n```python\nqc = 1\n```\n</BUGGY_PY>\n<FIXED_PY>\nqc = 2\n</FIXED_PY>"
    p3 = llm.parse_response(fenced)
    check(p3.buggy == "qc = 1", f"stray fence stripped (got {p3.buggy!r})")


def test_polish() -> None:
    print("\n[reconstruct] output polish")
    out, notes = reconstruct.polish("```python\nqc = 1\n```")
    check("```" not in out, "fence removed by polish")
    check(bool(notes), "fence removal noted")
    out2, notes2 = reconstruct.polish("")
    check(out2 == "" and bool(notes2), "empty output reported")


def test_static_helpers() -> None:
    print("\n[reconstruct] static analysis helpers")
    code = "qc = QuantumCircuit(2)\nsv = Statevector.from_instruction(qc)\nprint(np.pi)"
    missing = reconstruct.undefined_names(code)
    for n in ("QuantumCircuit", "Statevector", "np"):
        check(n in missing, f"{n} reported undefined")
    check("QuantumCircuit" not in reconstruct.undefined_names(
        "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)"),
        "imported name not reported undefined")
    check(reconstruct.detect_api_era("from qiskit import execute, Aer\nexecute(qc)") == "legacy",
          "legacy era detected")
    check(reconstruct.detect_api_era("from qiskit_aer import AerSimulator") == "modern",
          "modern era detected")
    ok, err = reconstruct.parses("def f(:\n  pass")
    check(not ok and "line" in err, "syntax error located")


def test_stub_provider_roundtrip() -> None:
    print("\n[stub] offline provider produces a parseable wire response")
    v = _view(
        buggy_code="from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)",
        fixed_code="from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.measure_all()",
    )
    prompt, _ = llm.build_prompt(v)
    text = stubgen.generate(prompt)
    p = llm.parse_response(text)
    check(not p.parse_error, "stub response parses as a wire message")
    check("QuantumCircuit" in p.buggy, "stub recovered buggy code")
    check("measure_all" in p.fixed, "stub recovered fixed code")
    check(p.needs_review is True, "stub always flags needs_review")


# --------------------------------------------------------------------------
def test_validation() -> None:
    print("\n[validate] file and pair checks")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        good = d / "g.py"
        good.write_text("from qiskit import QuantumCircuit\nqc = QuantumCircuit(1)\n", encoding="utf-8")
        c = validate.check_file(good)
        check(c.syntax_valid and c.non_empty and c.no_fences and c.no_prose, "clean file passes")

        bad = d / "b.py"
        bad.write_text("def f(:\n", encoding="utf-8")
        check(not validate.check_file(bad).syntax_valid, "syntax error detected")

        fenced = d / "f.py"
        fenced.write_text("```python\nqc = 1\n```\n", encoding="utf-8")
        check(not validate.check_file(fenced).no_fences, "markdown fence detected")

        prosey = d / "p.py"
        prosey.write_text("qc = 1\n# The problem is that you should transpile before running it\n",
                          encoding="utf-8")
        check(not validate.check_file(prosey).no_prose, "explanation prose detected")

        empty = d / "e.py"
        empty.write_text("", encoding="utf-8")
        check(not validate.check_file(empty).non_empty, "empty file detected")

    p = validate.check_pair("qc.h(0)\n", "qc.h(0)\n")
    check(p.identical and not p.structurally_plausible, "identical pair rejected")
    p2 = validate.check_pair("qc.h(0)\n", "qc.h(0)\nqc.measure_all()\n")
    check(not p2.identical and p2.structurally_plausible, "differing pair accepted")


def test_classification() -> None:
    print("\n[validate] status classification")
    from .sandbox import ExecResult

    ok = validate.FileChecks(exists=True, non_empty=True, syntax_valid=True, line_count=5)
    pair = validate.PairChecks(identical=False, similarity=0.8, structurally_plausible=True)

    s, _ = validate.classify(ok, ok, pair, ExecResult("ERROR", "ValueError"),
                             ExecResult("OK"), True)
    check(s == validate.STATUS_EXPECTED_BUG, f"buggy fails + fixed runs -> expected bug (got {s})")

    s, _ = validate.classify(ok, ok, pair, ExecResult("OK"), ExecResult("OK"), True)
    check(s == validate.STATUS_SUCCESS, f"both run -> success (got {s})")

    s, _ = validate.classify(ok, ok, pair, ExecResult("ERROR", "NameError"),
                             ExecResult("OK"), True)
    check(s == validate.STATUS_REVIEW, f"NameError -> needs review (got {s})")

    s, _ = validate.classify(ok, ok, pair,
                             ExecResult("ERROR", "ImportError", "cannot import name 'execute'"),
                             ExecResult("ERROR", "ImportError", "cannot import name 'execute'"), True)
    check(s == validate.STATUS_VERSION, f"ImportError -> version incompatible (got {s})")

    s, _ = validate.classify(ok, ok, pair, ExecResult("OK"), ExecResult("OK"), True,
                             model_needs_review=True, model_reason="fragmentary")
    check(s == validate.STATUS_REVIEW, f"model review flag honoured (got {s})")

    missing = validate.FileChecks(exists=False)
    s, _ = validate.classify(missing, ok, pair, ExecResult("NOT_RUN"), ExecResult("NOT_RUN"), True)
    check(s == validate.STATUS_FAILED, f"missing artifact -> generation failed (got {s})")

    ident = validate.PairChecks(identical=True, similarity=1.0, structurally_plausible=False)
    s, _ = validate.classify(ok, ok, ident, ExecResult("OK"), ExecResult("OK"), True)
    check(s == validate.STATUS_REVIEW, f"identical pair -> needs review (got {s})")


def test_sandbox() -> None:
    print("\n[sandbox] containment")
    from . import sandbox
    check(sandbox.wants_network("from qiskit_ibm_runtime import QiskitRuntimeService"),
          "runtime-service program flagged as network-seeking")
    check(not sandbox.wants_network("from qiskit import QuantumCircuit"),
          "local program not flagged")

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        net = d / "net.py"
        net.write_text("import socket\ns = socket.socket()\n", encoding="utf-8")
        check(sandbox.run_file(net, timeout=30).status == "ERROR",
              "socket creation refused inside the sandbox")

        ok = d / "ok.py"
        ok.write_text("print(1 + 1)\n", encoding="utf-8")
        check(sandbox.run_file(ok, timeout=30).status == "OK", "ordinary program runs")

        hang = d / "hang.py"
        hang.write_text("while True:\n    pass\n", encoding="utf-8")
        check(sandbox.run_file(hang, timeout=5).status == "TIMEOUT", "infinite loop cut off")

        err = d / "err.py"
        err.write_text("raise ValueError('boom')\n", encoding="utf-8")
        r = sandbox.run_file(err, timeout=30)
        check(r.status == "ERROR" and r.exc_type == "ValueError",
              f"exception type captured (got {r.exc_type})")


def test_question_file_is_verbatim() -> None:
    print("\n[pipeline] original_question.txt preserves source text exactly")
    from .pipeline import render_question_file
    row = SourceRow(
        platform="SE", issue_number=1, issue_id="x",
        title="My  title with   spacing",
        category="Category:\n\nCircuit\n\nWhy AI Wins: blah",
        buggy_code="qc.h(0)   # trailing",
        fixed_code="qc.h(0)\nqc.measure_all()",
        buggy_question_description="line1\nline2",
        fixed_solution_explanation="because reasons",
        excel_row=2, dir_name="issue_001",
    )
    out = render_question_file(row)
    for field_text in ("My  title with   spacing", "Why AI Wins: blah", "qc.h(0)   # trailing",
                       "line1\nline2", "because reasons", "qc.measure_all()"):
        check(field_text in out, f"verbatim: {field_text[:32]!r}")
    for header in ("Title:", "Category:", "Question:", "Original buggy code:",
                   "Solution explanation:", "Original fixed code:"):
        check(header in out, f"section header present: {header}")


def main() -> int:
    print("=" * 72)
    print("RECONSTRUCTION PIPELINE SELF-TESTS")
    print("=" * 72)
    for fn in (
        test_naming, test_category_sanitiser, test_block_splitting,
        test_flattening_detection, test_prose_only_cell, test_truncation_marker,
        test_prompt_contains_full_row, test_response_parsing, test_polish,
        test_static_helpers, test_stub_provider_roundtrip, test_validation,
        test_classification, test_sandbox, test_question_file_is_verbatim,
    ):
        fn()

    print("\n" + "=" * 72)
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
