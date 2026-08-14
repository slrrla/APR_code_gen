"""Orchestration: generate, validate and report on reconstructed APR cases.

Properties that matter for a 556-case run:

* **Isolated.** One case cannot abort the run; every case is wrapped and a
  failure becomes GENERATION_FAILED with the reason recorded.
* **Resumable.** Completed cases are checkpointed and skipped on re-run; raw
  model responses are cached, so a resumed run costs nothing for work already
  done.
* **Per-case context.** Each case is built from its own row and nothing else;
  no state is shared between cases.
"""
from __future__ import annotations

import csv
import json
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass

from . import config, sandbox, validate
from .loader import SourceRow, load_rows
from .reconstruct import reconstruct_case

REPORT_COLUMNS = [
    # required minimum
    "issue_number",
    "buggy_generated",
    "fixed_generated",
    "buggy_syntax_valid",
    "fixed_syntax_valid",
    "buggy_execution_status",
    "fixed_execution_status",
    "reconstruction_status",
    "notes",
    # provenance / diagnostics
    "case_dir",
    "issue_id",
    "platform",
    "api_era",
    "bug_summary",
    "fix_summary",
    "pair_similarity",
    "buggy_lines",
    "fixed_lines",
    "provider",
    "model",
    "cached",
    "repair_rounds",
    "input_tokens",
    "output_tokens",
    "source_truncated_fields",
]


@dataclass
class CaseResult:
    issue_number: int = 0
    buggy_generated: bool = False
    fixed_generated: bool = False
    buggy_syntax_valid: bool = False
    fixed_syntax_valid: bool = False
    buggy_execution_status: str = "NOT_RUN"
    fixed_execution_status: str = "NOT_RUN"
    reconstruction_status: str = validate.STATUS_FAILED
    notes: str = ""
    case_dir: str = ""
    issue_id: str = ""
    platform: str = ""
    api_era: str = ""
    bug_summary: str = ""
    fix_summary: str = ""
    pair_similarity: float = 0.0
    buggy_lines: int = 0
    fixed_lines: int = 0
    provider: str = ""
    model: str = ""
    cached: bool = False
    repair_rounds: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    source_truncated_fields: str = ""

    def row(self) -> dict:
        d = asdict(self)
        return {k: d[k] for k in REPORT_COLUMNS}


# --------------------------------------------------------------------------
# original_question.txt  (verbatim provenance)
# --------------------------------------------------------------------------
def render_question_file(row: SourceRow) -> str:
    """Exact spreadsheet text, in the required layout. Never summarised."""
    return (
        "Title:\n"
        f"{row.title}\n\n"
        "Category:\n"
        f"{row.category}\n\n"
        "Question:\n"
        f"{row.buggy_question_description}\n\n"
        "Original buggy code:\n"
        f"{row.buggy_code}\n\n"
        "Solution explanation:\n"
        f"{row.fixed_solution_explanation}\n\n"
        "Original fixed code:\n"
        f"{row.fixed_code}\n"
    )


# --------------------------------------------------------------------------
# One case
# --------------------------------------------------------------------------
def write_provenance(row: SourceRow):
    """Create the case directory and write original_question.txt."""
    case_dir = config.OUTPUT_DIR / row.dir_name
    case_dir.mkdir(parents=True, exist_ok=True)
    qp = case_dir / config.QUESTION_FILE
    qp.write_text(render_question_file(row), encoding="utf-8")
    return case_dir, qp


def finalize_case(row: SourceRow, pair, execute: bool = True) -> CaseResult:
    """Write, validate, execute and classify an already-reconstructed pair.

    Shared by every reconstruction route: provider-driven or produced by the
    Claude Code agent itself. ``pair`` is a ``reconstruct.PairResult``.
    """
    res = CaseResult(
        issue_number=row.issue_number,
        case_dir=row.dir_name,
        issue_id=row.issue_id,
        platform=row.platform,
        source_truncated_fields="|".join(row.truncated_fields),
    )
    notes: list[str] = []
    if row.truncated_fields:
        notes.append("source cell hit the Excel 32767-char limit and is truncated: "
                     + ", ".join(row.truncated_fields))

    case_dir, question_path = write_provenance(row)
    buggy_path = case_dir / config.BUGGY_FILE
    fixed_path = case_dir / config.FIXED_FILE

    res.provider, res.model = pair.provider, pair.model
    res.cached, res.repair_rounds = pair.cached, pair.repair_rounds
    res.input_tokens, res.output_tokens = pair.input_tokens, pair.output_tokens
    res.api_era = pair.api_era
    res.bug_summary, res.fix_summary = pair.bug_summary, pair.fix_summary
    notes.extend(pair.notes)

    if pair.failed:
        res.reconstruction_status = validate.STATUS_FAILED
        res.notes = " | ".join(dict.fromkeys(n for n in notes if n))[:1200]
        return res

    buggy_path.write_text(pair.buggy, encoding="utf-8")
    fixed_path.write_text(pair.fixed, encoding="utf-8")
    res.buggy_generated = bool(pair.buggy.strip())
    res.fixed_generated = bool(pair.fixed.strip())

    bchecks = validate.check_file(buggy_path)
    fchecks = validate.check_file(fixed_path)
    res.buggy_syntax_valid = bchecks.syntax_valid
    res.fixed_syntax_valid = fchecks.syntax_valid
    res.buggy_lines, res.fixed_lines = bchecks.line_count, fchecks.line_count

    pchecks = validate.check_pair(pair.buggy, pair.fixed)
    res.pair_similarity = pchecks.similarity

    if execute and bchecks.syntax_valid and fchecks.syntax_valid:
        bexec = sandbox.run_file(buggy_path)
        fexec = sandbox.run_file(fixed_path)
    else:
        bexec = sandbox.ExecResult("NOT_RUN")
        fexec = sandbox.ExecResult("NOT_RUN")
    res.buggy_execution_status = bexec.summary
    res.fixed_execution_status = fexec.summary

    status, cnotes = validate.classify(
        bchecks, fchecks, pchecks, bexec, fexec, question_path.exists(),
        model_needs_review=pair.needs_review, model_reason=pair.review_reason,
    )
    res.reconstruction_status = status
    notes.extend(cnotes)
    res.notes = " | ".join(dict.fromkeys(n for n in notes if n))[:1200]
    return res


def process_case(row: SourceRow, provider, execute: bool = True,
                 use_cache: bool = True) -> CaseResult:
    """Provider-driven route: reconstruct via an API provider, then finalize."""
    pair = reconstruct_case(row.view(), provider, use_cache=use_cache)
    return finalize_case(row, pair, execute=execute)


# --------------------------------------------------------------------------
# Checkpointing
# --------------------------------------------------------------------------
_lock = threading.Lock()


def load_checkpoint() -> dict[str, dict]:
    if not config.CHECKPOINT.exists():
        return {}
    done: dict[str, dict] = {}
    for line in config.CHECKPOINT.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        done[rec.get("case_dir", "")] = rec
    done.pop("", None)
    return done


def append_checkpoint(result: CaseResult) -> None:
    config.STATE_DIR.mkdir(parents=True, exist_ok=True)
    with _lock:
        with config.CHECKPOINT.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(result.row(), ensure_ascii=False) + "\n")


#: A case in one of these states is done and is not regenerated on resume.
TERMINAL_OK = {
    validate.STATUS_SUCCESS,
    validate.STATUS_EXPECTED_BUG,
    validate.STATUS_VERSION,
    validate.STATUS_REVIEW,
}


# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------
def run(
    provider,
    rows: list[SourceRow] | None = None,
    execute: bool = True,
    force: bool = False,
    workers: int = 6,
    progress_every: int = 25,
    use_cache: bool = True,
) -> list[CaseResult]:
    rows = rows if rows is not None else load_rows()
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.STATE_DIR.mkdir(parents=True, exist_ok=True)

    done = {} if force else load_checkpoint()
    todo = [r for r in rows
            if force or done.get(r.dir_name, {}).get("reconstruction_status") not in TERMINAL_OK]
    skipped = len(rows) - len(todo)
    if skipped:
        print(f"resuming: {skipped} case(s) already complete, {len(todo)} to process")

    results: list[CaseResult] = []
    completed = 0

    def work(row: SourceRow) -> CaseResult:
        try:
            return process_case(row, provider, execute=execute, use_cache=use_cache)
        except Exception as exc:  # isolation: a bad case never kills the run
            return CaseResult(
                issue_number=row.issue_number,
                case_dir=row.dir_name,
                issue_id=row.issue_id,
                platform=row.platform,
                reconstruction_status=validate.STATUS_FAILED,
                notes=f"pipeline exception: {type(exc).__name__}: {exc} :: "
                      + traceback.format_exc(limit=2).replace("\n", " ")[:400],
            )

    if todo:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = {pool.submit(work, r): r for r in todo}
            for fut in as_completed(futures):
                res = fut.result()
                append_checkpoint(res)
                results.append(res)
                completed += 1
                if progress_every and completed % progress_every == 0:
                    print(f"  {completed}/{len(todo)} processed")

    merged = {r.case_dir: r.row() for r in results}
    for name, rec in load_checkpoint().items():
        merged.setdefault(name, rec)

    order = {r.dir_name: i for i, r in enumerate(rows)}
    ordered = sorted(merged.values(), key=lambda d: order.get(d.get("case_dir", ""), 10**9))
    write_report(ordered)
    return results


def write_report(rows: list[dict]) -> None:
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with config.REPORT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=REPORT_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in REPORT_COLUMNS})
    print(f"report written: {config.REPORT_CSV}")
