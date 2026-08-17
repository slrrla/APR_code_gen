#!/usr/bin/env python3
"""
generate_tests.py  --  PART 1 of 2 (generation ONLY)

Reads buggy_*.py / fixed_*.py in each case folder and has Claude (Opus) write ONE
deterministic differential oracle `test.py` per case.

This step does NOT run anything: no pytest, no qiskit, no environment needed.
It only needs ANTHROPIC_API_KEY. All execution / validation (which requires the
per-version Qiskit envs) lives in validate_versions.py.

    # all cases under --root:
    ANTHROPIC_API_KEY=...  python generate_test.py --root reconstructed_cases

    # only the first N valid cases listed in the xlsx (per-case floor version
    # taken from that case's own reproduced-Versions column):
    ANTHROPIC_API_KEY=...  python generate_test.py --xlsx Valid_cases.xlsx --first 5

--floor-version is passed to the LLM as the OLDEST target Qiskit version, so the
generated oracle only uses APIs available across all your target versions. When
--xlsx is given, each case's floor version is the oldest version in its own
'Versions' cell (falls back to --floor-version if the cell is empty).
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from anthropic import Anthropic

MODEL = "claude-opus-5"   # Opus 5.0. Swap to whichever Opus string you can call.
MAX_TOKENS = 16000  # Opus 5 emits thinking blocks before the code; leave headroom

# ---------------------------------------------------------------------------
# Prompt (every rule we agreed on)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = r"""You are an expert in quantum software testing, Qiskit internals, and
automatic program repair (APR). You write rigorous, DETERMINISTIC software tests for real
Qiskit bug cases, in the unittest style of the Bugs4Q benchmark.

Inputs for ONE case: the buggy source, the human fixed source, the OLDEST target Qiskit
version, and (when available) INTENT CONTEXT = the original GitHub issue title/body and the
bug Type. USE THE INTENT CONTEXT FIRST to understand what the program is SUPPOSED to do; fall
back to reasoning over the buggy-vs-fixed diff only when no issue context is given.

Produce ONE `unittest`-based `test.py` (pytest discovers it) that asserts the program's
INTENDED behavior as CONCRETE expected values, like a normal unit test:

    def add(a, b): return a + b
    def test_add(): assert add(1, 2) == 3      # the 3 comes from KNOWING the intent

=== STYLE: emulate Bugs4Q ===
Bugs4Q tests use unittest.TestCase with explicit assertions and a __main__ guard. Example
(a crash-type bug):

    import unittest
    class Test(unittest.TestCase):
        def test_b1(self):
            try:
                from qiskit import QuantumCircuit
                qc = QuantumCircuit(3)
                qc.cx(0, 1, label='Label', ctrl_state=0)
                qc.ccx(0, 1, 2, label='Label', ctrl_state=1)
            except TypeError as e:
                self.assertEqual(type(e), TypeError)
            else:
                self.fail('TypeError not raised')
    if __name__ == '__main__':
        unittest.main(argv=[''])

Match this FLAVOR (unittest.TestCase, the __main__ guard). But the real Bugs4Q tests have two
flaws you MUST fix:

=== TWO REQUIRED ADAPTATIONS ===
1. DO NOT EMBED the code. Bugs4Q hardcodes the snippet, so one test judges only one version.
   Instead load the code under test from os.environ["MUT"] (default: the sibling fixed file)
   via runpy.run_path, so the SAME test judges the buggy file, the human fix, OR any LLM
   candidate patch.
2. THE CORRECT VERSION MUST PASS. Bugs4Q's "fixed" test sometimes still expects the error to
   be raised (e.g. the ctrl_state example: the fixed code actually runs fine, yet its test
   demands a TypeError, so it wrongly fails on the real fix). Your test must PASS when the
   code runs correctly and FAIL only on the buggy behavior.

=== WHAT TO ASSERT (concrete, intent-derived) ===
- WRONG_OUTPUT: assert the intended probability distribution / statevector. State the expected
  values from the intent (do NOT rebuild a reference circuit to compare against). e.g.
  self.assertAlmostEqual per probability, or assertTrue(sv.equiv(Statevector([...]))).
- CRASH: loading the buggy file via runpy raises -> that propagation IS the failure signal,
  so the bug is detected. The correct version must run AND produce the intended observable --
  assert that observable, not merely "did not raise".
- STRUCTURAL: assert concrete circuit properties (num_qubits, ordered op names/params,
  circuit.name, QASM).

=== HARD RULES ===
- Deterministic only; never assert raw shot counts (seed + ideal probabilities + tolerance if
  sampling is truly unavoidable). Little-endian (rightmost char = qubit 0). Use ONLY APIs in
  the given oldest target version. No network/IBMQ/hardware/credentials/plotting; replace
  remote backends with local Statevector/Operator; if impossible offline, skip with reason.
- CONTRACT: PASS when MUT is the fixed file, FAIL when MUT is the buggy file.
- OUTPUT ONLY the Python code for test.py. No markdown fences, no commentary, no prose.

=== SKELETON (adapt; keep MUT; assert CONCRETE intent-derived values) ===

# intent: <one line, taken from the issue/Type>
# bug_type: <CRASH|WRONG_OUTPUT|STRUCTURAL>
import os, runpy, unittest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "<FIXED_FILENAME>"))  # code under test

def _circuit(path):
    ns = runpy.run_path(path)            # buggy version raises here -> test fails (bug found)
    cs = [v for v in ns.values() if isinstance(v, QuantumCircuit)]
    assert cs, "no QuantumCircuit produced by the script"
    return cs[-1]

class Test(unittest.TestCase):
    def test_intent(self):
        qc = _circuit(MUT)
        sv = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
        probs = sv.probabilities_dict()
        # INTENT: <e.g. Bell pair on q0,q1 -> only '00' and '11', each 0.5>
        self.assertEqual(set(probs), {'00', '11'})
        for k in ('00', '11'):
            self.assertAlmostEqual(probs[k], 0.5, places=9)

if __name__ == '__main__':
    unittest.main(argv=[''])
"""

USER_TEMPLATE = """Oldest target Qiskit version: {version}
Fixed filename (use as the default MUT path in the skeleton): {fixed_name}

=== INTENT CONTEXT (use FIRST to infer what the program SHOULD do) ===
{intent_context}

=== BUGGY SOURCE ({buggy_name}) ===
{buggy_src}

=== FIXED / GROUND-TRUTH SOURCE ({fixed_name}) ===
{fixed_src}

Write test.py in Bugs4Q unittest style, but with MUT indirection and a CORRECT oracle
(PASS on the fixed code, FAIL on the buggy code). Output ONLY the code."""


def find_pair(case_dir: Path):
    """Locate buggy/fixed sources, tolerant of casing (buggy.py / Buggy.py,
    fixed.py / Fixed.py / Fix.py). Ignores test.py and modify files (Mod.py)."""
    pys = [p for p in case_dir.iterdir()
           if p.is_file() and p.suffix.lower() == ".py" and p.name.lower() != "test.py"]

    def pick(prefix):
        cands = sorted((p for p in pys if p.stem.lower().startswith(prefix)),
                       key=lambda p: (len(p.stem), p.name.lower()))
        if len(cands) > 1:
            print(f"  [warn] {case_dir.name}: multiple '{prefix}*.py' "
                  f"{[c.name for c in cands]}; using {cands[0].name}", file=sys.stderr)
        return cands[0] if cands else None

    return pick("bug"), pick("fix")


def strip_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip() + "\n"


def read_intent_context(case_dir: Path) -> str:
    """Combine original_question.txt (preferred), issue_content.txt and
    readme_content.txt if present, so the LLM sees the original SE/SO question."""
    parts = []
    for name in ("original_question.txt", "issue_content.txt", "readme_content.txt"):
        f = case_dir / name
        if f.exists():
            parts.append(f"[{name}]\n{f.read_text(encoding='utf-8', errors='replace').strip()}")
    return "\n\n".join(parts) if parts else "(no issue/README context available; infer intent from the code diff)"


def call_llm(client: Anthropic, version, buggy, fixed, intent_context) -> str:
    resp = client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": USER_TEMPLATE.format(
            version=version, buggy_name=buggy.name, fixed_name=fixed.name,
            intent_context=intent_context,
            buggy_src=buggy.read_text(encoding="utf-8", errors="replace"),
            fixed_src=fixed.read_text(encoding="utf-8", errors="replace"))}],
    )
    return strip_fences("".join(b.text for b in resp.content if b.type == "text"))


def _version_key(v: str):
    return tuple(int(x) for x in v.strip().split("."))


def load_xlsx_cases(xlsx_path: Path, root: Path, first=None, default_version="0.25.0"):
    """Read Valid_cases.xlsx (Case_number | Check | Versions) and map each row to
    its case folder(s). Returns [(case_dir, floor_version), ...] in xlsx order.

    Folder naming: issue_NNN (zero-padded to 3) with optional _se / _so variants.
    If a case number maps to BOTH _se and _so and the xlsx row doesn't say which,
    both are generated and a warning is printed (resolve by adding a Source column)."""
    import openpyxl  # local import: only needed in --xlsx mode
    rows = list(openpyxl.load_workbook(xlsx_path).active.iter_rows(values_only=True))[1:]
    if first is not None:
        rows = rows[:first]
    out, seen = [], set()
    for row in rows:
        case_no, versions = int(row[0]), str(row[2] or "")
        vers = [v.strip() for v in versions.split(",") if v.strip()]
        floor = min(vers, key=_version_key) if vers else default_version
        base = f"issue_{case_no:03d}"
        cands = [root / n for n in (base, f"{base}_se", f"{base}_so") if (root / n).is_dir()]
        if not cands:
            print(f"  [warn] case {case_no}: no folder '{base}[_se|_so]' under {root}", file=sys.stderr)
            continue
        if len(cands) > 1:
            print(f"  [warn] case {case_no}: both _se and _so exist; generating for "
                  f"{[c.name for c in cands]} (add a Source column to disambiguate)", file=sys.stderr)
        for c in cands:
            if c.name not in seen:      # xlsx has duplicate rows for some cases
                seen.add(c.name)
                out.append((c, floor))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="reconstructed_cases")
    ap.add_argument("--floor-version", default="0.25.0", dest="version",
                    help="oldest target Qiskit version (prompt context for API compatibility)")
    ap.add_argument("--only", default=None, help="comma-separated case folder names")
    ap.add_argument("--xlsx", default=None,
                    help="Valid_cases.xlsx: generate only for the cases listed there, "
                         "using each case's own oldest reproduced version as the floor")
    ap.add_argument("--first", type=int, default=None,
                    help="with --xlsx: only the first N rows")
    args = ap.parse_args()

    root = Path(args.root)
    client = Anthropic()  # reads ANTHROPIC_API_KEY
    only = set(args.only.split(",")) if args.only else None

    if args.xlsx:
        cases = load_xlsx_cases(Path(args.xlsx), root, args.first, args.version)
    else:
        cases = [(d, args.version) for d in sorted(p for p in root.iterdir() if p.is_dir())]

    report = []
    for case_dir, floor_version in cases:
        if only and case_dir.name not in only:
            continue
        buggy, fixed = find_pair(case_dir)
        if not buggy or not fixed:
            report.append({"case": case_dir.name, "status": "missing_pair"})
            print(f"[skip] {case_dir.name}: buggy/fixed not found")
            continue
        try:
            intent_context = read_intent_context(case_dir)
            code = call_llm(client, floor_version, buggy, fixed, intent_context)
            (case_dir / "test.py").write_text(code, encoding="utf-8")
            status = "generated"
        except Exception as e:  # noqa: BLE001 - keep the batch going
            status = f"llm_error: {e}"
        has_ctx = any((case_dir / n).exists()
                      for n in ("original_question.txt", "issue_content.txt", "readme_content.txt"))
        report.append({"case": case_dir.name, "status": status, "intent_context": has_ctx,
                       "floor_version": floor_version, "buggy": buggy.name, "fixed": fixed.name})
        print(f"[{case_dir.name}] {status}" + ("" if has_ctx else "  (no intent context)"))

    (root / "generation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\n=== GENERATION SUMMARY ===")
    for k, v in Counter(r["status"].split(":")[0] for r in report).items():
        print(f"  {k}: {v}")
    print(f"\nWrote test.py per case + {root/'generation_report.json'}")
    print("Next: set up the per-version envs and run validate_versions.py to gate them.")


if __name__ == "__main__":
    main()