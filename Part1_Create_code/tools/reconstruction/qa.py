"""Dataset-level QA over the generated corpus.

Reads the artifacts back off disk rather than trusting the in-memory run, so
this catches truncated writes, stray directories and post-hoc edits too.
"""
from __future__ import annotations

import ast
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

from . import config, validate
from .loader import load_rows


def _read_report() -> list[dict]:
    if not config.REPORT_CSV.exists():
        return []
    with config.REPORT_CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def run_qa(verbose: bool = True) -> dict:
    rows = load_rows()
    report = _read_report()
    by_dir = {r["case_dir"]: r for r in report}

    expected_dirs = {r.dir_name for r in rows}
    present_dirs = {
        p.name for p in config.OUTPUT_DIR.iterdir()
        if p.is_dir() and p.name.startswith("issue_")
    } if config.OUTPUT_DIR.exists() else set()

    findings: dict[str, list] = defaultdict(list)

    # -- structural ------------------------------------------------------
    findings["missing_directories"] = sorted(expected_dirs - present_dirs)
    findings["unexpected_directories"] = sorted(present_dirs - expected_dirs)

    issue_counts = Counter(r.issue_number for r in rows)
    findings["duplicate_issue_numbers"] = sorted(
        f"{n} (x{c})" for n, c in issue_counts.items() if c > 1
    )
    nums = sorted(issue_counts)
    findings["issue_number_gaps_count"] = [
        len(set(range(nums[0], nums[-1] + 1)) - set(nums))
    ]

    # -- per-case artifact checks ----------------------------------------
    empty_py, syntax_fail, fenced, prose, oversized, identical = [], [], [], [], [], []
    missing_files = []
    for r in rows:
        d = config.OUTPUT_DIR / r.dir_name
        b, f, q = (d / config.BUGGY_FILE, d / config.FIXED_FILE, d / config.QUESTION_FILE)
        for label, p in (("buggy.py", b), ("fixed.py", f), ("original_question.txt", q)):
            if not p.exists():
                missing_files.append(f"{r.dir_name}/{label}")
        if not (b.exists() and f.exists()):
            continue

        bsrc = b.read_text(encoding="utf-8", errors="replace")
        fsrc = f.read_text(encoding="utf-8", errors="replace")

        for label, src, path in (("buggy.py", bsrc, b), ("fixed.py", fsrc, f)):
            checks = validate.check_file(path)
            if not checks.non_empty:
                empty_py.append(f"{r.dir_name}/{label}")
            if not checks.syntax_valid:
                syntax_fail.append(f"{r.dir_name}/{label}: {checks.syntax_error}")
            if not checks.no_fences:
                fenced.append(f"{r.dir_name}/{label}")
            if not checks.no_prose:
                prose.append(f"{r.dir_name}/{label}: {checks.prose_evidence[:60]}")
            if checks.oversized:
                oversized.append(f"{r.dir_name}/{label} ({checks.line_count} lines)")

        pair = validate.check_pair(bsrc, fsrc)
        if pair.identical:
            identical.append(r.dir_name)

    findings["missing_files"] = missing_files
    findings["empty_python_files"] = empty_py
    findings["syntax_failures"] = syntax_fail
    findings["markdown_contamination"] = fenced
    findings["prose_contamination"] = prose
    findings["oversized_programs"] = oversized
    findings["identical_pairs"] = identical

    # -- status distribution ---------------------------------------------
    status_counts = Counter(r["reconstruction_status"] for r in report)
    findings["generation_failures"] = [
        r["case_dir"] for r in report
        if r["reconstruction_status"] == validate.STATUS_FAILED
    ]
    findings["needs_review"] = [
        r["case_dir"] for r in report
        if r["reconstruction_status"] == validate.STATUS_REVIEW
    ]
    leak = [r["case_dir"] for r in report if "leakage" in (r.get("notes") or "").lower()]
    findings["leak_suspected"] = leak

    summary = {
        "source_rows": len(rows),
        "expected_directories": len(expected_dirs),
        "directories_on_disk": len(present_dirs),
        "report_rows": len(report),
        "status_counts": dict(status_counts),
        "findings": {k: v for k, v in findings.items()},
    }

    if verbose:
        _print(summary, findings, status_counts, rows, report)
    return summary


def _print(summary, findings, status_counts, rows, report) -> None:
    line = "=" * 72
    print(line)
    print("DATASET QA")
    print(line)
    print(f"source rows in {config.SOURCE_SHEET:<24s} : {summary['source_rows']}")
    print(f"expected case directories             : {summary['expected_directories']}")
    print(f"case directories on disk              : {summary['directories_on_disk']}")
    print(f"rows in reconstruction_report.csv     : {summary['report_rows']}")

    print("\nreconstruction_status distribution")
    total = max(1, sum(status_counts.values()))
    for st in (validate.STATUS_SUCCESS, validate.STATUS_EXPECTED_BUG,
               validate.STATUS_VERSION, validate.STATUS_REVIEW, validate.STATUS_FAILED):
        n = status_counts.get(st, 0)
        print(f"  {st:<28s} {n:5d}  ({100*n/total:5.1f}%)")
    other = {k: v for k, v in status_counts.items() if k not in {
        validate.STATUS_SUCCESS, validate.STATUS_EXPECTED_BUG, validate.STATUS_VERSION,
        validate.STATUS_REVIEW, validate.STATUS_FAILED}}
    for k, v in other.items():
        print(f"  {k:<28s} {v:5d}  (unexpected status)")

    print("\nexecution outcomes")
    for col in ("buggy_execution_status", "fixed_execution_status"):
        c = Counter(r[col] for r in report)
        print(f"  {col}")
        for k, v in c.most_common(8):
            print(f"      {k:<26s} {v:5d}")

    print("\nintegrity findings")
    order = [
        ("missing_directories", "case directories missing from disk"),
        ("unexpected_directories", "directories not traceable to a source row"),
        ("missing_files", "required artifact files missing"),
        ("empty_python_files", "empty generated Python files"),
        ("syntax_failures", "Python files that do not parse"),
        ("markdown_contamination", "files still containing markdown fences"),
        ("prose_contamination", "files containing answer/explanation prose"),
        ("identical_pairs", "buggy.py identical to fixed.py"),
        ("oversized_programs", f"programs over {config.MAX_REASONABLE_LINES} lines"),
        ("leak_suspected", "cases flagged by the leakage audit"),
        ("generation_failures", "GENERATION_FAILED cases"),
        ("needs_review", "NEEDS_REVIEW cases"),
    ]
    for key, label in order:
        items = findings.get(key, [])
        mark = "ok  " if not items else "FLAG"
        print(f"  [{mark}] {label:<48s} {len(items)}")
        if items and key not in ("needs_review", "generation_failures", "leak_suspected"):
            for it in items[:5]:
                print(f"           - {it}")
            if len(items) > 5:
                print(f"           ... and {len(items)-5} more")

    dupes = findings.get("duplicate_issue_numbers", [])
    print(f"\nsource issue_number duplicates        : {len(dupes)}"
          f"  (resolved by NAMING_SCHEME={config.NAMING_SCHEME!r})")
    print(f"source issue_number gaps preserved    : "
          f"{findings.get('issue_number_gaps_count', [0])[0]}")
    print(line)


if __name__ == "__main__":
    s = run_qa()
    bad = sum(len(s["findings"].get(k, [])) for k in
              ("missing_directories", "missing_files", "empty_python_files",
               "syntax_failures", "markdown_contamination", "identical_pairs"))
    sys.exit(1 if bad else 0)
