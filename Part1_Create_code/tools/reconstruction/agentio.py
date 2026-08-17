"""Handoff between the pipeline and the Claude Code agent doing reconstruction.

No external model API is involved. The pipeline emits a worklist of pending
cases; the agent reads it, reconstructs each pair in-session, and writes the
results back in the same wire format the parser already understands. Ingest
then validates, executes, classifies, checkpoints and reports.

    run agent-next   --count N     -> .state/worklist/batch_NNN.md
    (agent reconstructs)           -> .state/responses/batch_NNN.md
    run agent-ingest --file <path> -> artifacts + report + checkpoint
"""
from __future__ import annotations

import re
from pathlib import Path

from . import config, llm, pipeline, validate
from .loader import SourceRow, load_rows
from .reconstruct import PairResult

WORKLIST_DIR = config.STATE_DIR / "worklist"
RESPONSE_DIR = config.STATE_DIR / "responses"

CASE_RE = re.compile(r"^===\s*CASE\s+(\S+)\s*===\s*$", re.M)

INSTRUCTIONS = """\
# Reconstruction worklist

You are reconstructing ground-truth bug/fix pairs for an APR dataset. Reason
over the WHOLE of each case below: the fix explains what the question was
really about, and the question explains what the fix is correcting.

The scraped code is damaged. Expect newlines stripped so statements run
together on one line, blocks concatenated, prose mixed into code fields,
fragments that are only a symbol name, and truncation. Recover the program the
author actually ran.

For each case produce two programs.

buggy.py
  - minimal, self-contained, reproduces the reported problem
  - PRESERVE THE BUG. Never repair it. If the defect is a missing or wrong
    import, it stays missing or wrong.
  - add only the scaffolding needed to reach the buggy behaviour

fixed.py
  - same conceptual task with the reported correction applied
  - change only what the fix requires; keep structure, names and ordering
    aligned with buggy.py so the diff isolates the repair

Both
  - valid Python, no markdown fences, no prose or commentary
  - as small as practical while still executable
  - PRESERVE THE QISKIT ERA of the case (0.x execute()/Aer/IBMQ/QuantumInstance
    stays 0.x). Do not modernise and do not backport. Version mismatch is
    recorded separately and is not yours to solve.
  - never contact a real backend; prefer local simulators
  - do not fabricate datasets, expected outputs or fake results. Deterministic
    placeholder values are fine when a value is missing and is needed to run,
    provided the placeholder does not change the bug.

If the source is too incomplete to reconstruct faithfully, do NOT invent an
elaborate program. Produce the most conservative reconstruction the evidence
supports and set needs_review: true with a short reason.

Write your answers to the matching file under .state/responses/ using exactly
this format, one block per case:

=== CASE <case_dir> ===
<BUGGY_PY>
(python source)
</BUGGY_PY>
<FIXED_PY>
(python source)
</FIXED_PY>
<META>
needs_review: true|false
api_era: legacy|modern|unknown
bug_summary: one line
fix_summary: one line
reason: required when needs_review is true
</META>

"""


# --------------------------------------------------------------------------
def pending_rows(rows: list[SourceRow], force: bool = False) -> list[SourceRow]:
    done = {} if force else pipeline.load_checkpoint()
    return [r for r in rows
            if force or done.get(r.dir_name, {}).get("reconstruction_status")
            not in pipeline.TERMINAL_OK]


def next_batch_index() -> int:
    WORKLIST_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(WORKLIST_DIR.glob("batch_*.md"))
    return len(existing) + 1


def write_worklist(count: int, force: bool = False,
                   only: list[str] | None = None) -> tuple[Path, list[str]]:
    rows = load_rows()
    if only:
        want = set(only)
        sel = [r for r in rows if r.dir_name in want]
    else:
        sel = pending_rows(rows, force)[:count]

    idx = next_batch_index()
    path = WORKLIST_DIR / f"batch_{idx:03d}.md"
    RESPONSE_DIR.mkdir(parents=True, exist_ok=True)

    parts = [INSTRUCTIONS,
             f"Write results to: .state/responses/batch_{idx:03d}.md",
             f"Cases in this batch: {len(sel)}", ""]
    for r in sel:
        prompt, _ = llm.build_prompt(r.view())
        parts.append(f"\n\n{'=' * 70}\n=== CASE {r.dir_name} ===\n{'=' * 70}\n{prompt}")
    path.write_text("\n".join(parts), encoding="utf-8")
    return path, [r.dir_name for r in sel]


# --------------------------------------------------------------------------
def parse_batch(text: str) -> dict[str, llm.ParsedPair]:
    """Split an agent response file into per-case parsed pairs."""
    out: dict[str, llm.ParsedPair] = {}
    marks = list(CASE_RE.finditer(text))
    for i, m in enumerate(marks):
        case = m.group(1).strip()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[case] = llm.parse_response(text[m.end():end])
    return out


def ingest(path: Path, execute: bool = True) -> list[pipeline.CaseResult]:
    text = Path(path).read_text(encoding="utf-8")
    parsed = parse_batch(text)
    if not parsed:
        raise SystemExit(f"no '=== CASE <dir> ===' blocks found in {path}")

    rows = {r.dir_name: r for r in load_rows()}
    unknown = [c for c in parsed if c not in rows]
    if unknown:
        raise SystemExit(f"unknown case id(s) in {path}: {unknown[:5]}")

    results: list[pipeline.CaseResult] = []
    for case, p in parsed.items():
        row = rows[case]
        pair = PairResult(
            buggy=p.buggy, fixed=p.fixed,
            needs_review=p.needs_review, review_reason=p.reason,
            api_era=p.api_era, bug_summary=p.bug_summary, fix_summary=p.fix_summary,
            provider="claude-code-agent", model="claude-code-session",
        )
        if p.parse_error:
            pair.failed = True
            pair.failure = p.parse_error
            pair.notes.append(p.parse_error)
        from .reconstruct import polish
        if not pair.failed:
            pair.buggy, n1 = polish(p.buggy)
            pair.fixed, n2 = polish(p.fixed)
            pair.notes.extend(n1 + n2)

        res = pipeline.finalize_case(row, pair, execute=execute)
        pipeline.append_checkpoint(res)
        results.append(res)

    rebuild_report()
    return results


def rebuild_report() -> None:
    rows = load_rows()
    order = {r.dir_name: i for i, r in enumerate(rows)}
    merged = pipeline.load_checkpoint()
    ordered = sorted(merged.values(), key=lambda d: order.get(d.get("case_dir", ""), 10**9))
    pipeline.write_report(ordered)


def revalidate(execute: bool = True, only: list[str] | None = None) -> list[pipeline.CaseResult]:
    """Re-run validation, execution and classification over existing artifacts.

    Reconstruction is never repeated: buggy.py/fixed.py are read back off disk
    and the model's own metadata is carried forward from the checkpoint. Use
    after an environment change (installing qiskit-aer, upgrading Qiskit) so
    execution-derived statuses reflect the new environment.
    """
    rows = {r.dir_name: r for r in load_rows()}
    done = pipeline.load_checkpoint()
    want = set(only) if only else None

    results: list[pipeline.CaseResult] = []
    for case, rec in done.items():
        if want and case not in want:
            continue
        row = rows.get(case)
        if row is None:
            continue
        d = config.OUTPUT_DIR / case
        bp, fp = d / config.BUGGY_FILE, d / config.FIXED_FILE
        if not (bp.exists() and fp.exists()):
            continue
        pair = PairResult(
            buggy=bp.read_text(encoding="utf-8", errors="replace"),
            fixed=fp.read_text(encoding="utf-8", errors="replace"),
            api_era=rec.get("api_era", "unknown"),
            bug_summary=rec.get("bug_summary", ""),
            fix_summary=rec.get("fix_summary", ""),
            provider=rec.get("provider", ""),
            model=rec.get("model", ""),
        )
        # Preserve a review flag the reconstructor raised about the source.
        note = rec.get("notes", "") or ""
        if "flagged during reconstruction:" in note:
            pair.needs_review = True
            pair.review_reason = note.split("flagged during reconstruction:", 1)[1].strip()[:300]
        res = pipeline.finalize_case(row, pair, execute=execute)
        pipeline.append_checkpoint(res)
        results.append(res)

    rebuild_report()
    return results


def status() -> dict:
    rows = load_rows()
    done = pipeline.load_checkpoint()
    counts: dict[str, int] = {}
    for rec in done.values():
        s = rec.get("reconstruction_status", "?")
        counts[s] = counts.get(s, 0) + 1
    pend = pending_rows(rows)
    return {
        "total": len(rows),
        "checkpointed": len(done),
        "pending": len(pend),
        "status_counts": counts,
        "next_pending": [r.dir_name for r in pend[:10]],
    }
