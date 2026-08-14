"""Export the execution matrix: long-format CSV plus the Excel workbook."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import pandas as pd

from . import classify, config, envs, runner
from .versions import VERSIONS, all_versions

CSV_COLUMNS = [
    "issue_number", "issue_id", "platform", "case_directory",
    "qiskit_version", "python_version",
    "buggy_status", "buggy_exit_code", "buggy_runtime_seconds",
    "buggy_stdout", "buggy_stderr", "buggy_reason",
    "fixed_status", "fixed_exit_code", "fixed_runtime_seconds",
    "fixed_stdout", "fixed_stderr", "fixed_reason",
    "behavioral_bug_reproduced", "behavioral_fix_verified", "behavioral_evidence",
    "pair_classification", "ground_truth_confirmed", "notes",
]

#: Excel caps a cell at 32767 characters; keep well clear and leave the full
#: text to the CSV.
_EXCEL_CELL = 1000


def _load_frame() -> pd.DataFrame:
    rows = list(runner.load_results().values())
    if not rows:
        return pd.DataFrame(columns=CSV_COLUMNS)
    df = pd.DataFrame(rows)
    for col in CSV_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[CSV_COLUMNS]


def write_csv(df: pd.DataFrame) -> Path:
    df.to_csv(config.EXECUTION_CSV, index=False, encoding="utf-8")
    return config.EXECUTION_CSV


# --------------------------------------------------------------------------
def _best_row(group: pd.DataFrame) -> pd.Series:
    """Best reproduction version for one case, by the documented preference."""
    def rank(r) -> tuple:
        gt = bool(r["ground_truth_confirmed"])
        valid = r["pair_classification"] == classify.VALID_REPAIR
        fixed_pass = r["fixed_status"] == classify.PASS
        behav = r["behavioral_fix_verified"] == "YES"
        evaluable = r["pair_classification"] != classify.NOT_EVALUABLE
        return (gt, valid, fixed_pass and behav, fixed_pass, evaluable)

    ordered = sorted(group.to_dict("records"), key=rank, reverse=True)
    return pd.Series(ordered[0])


def build_case_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    out = []
    for case, group in df.groupby("case_directory"):
        best = _best_row(group)
        valid_versions = group.loc[
            group["pair_classification"] == classify.VALID_REPAIR, "qiskit_version"].tolist()
        gt_versions = group.loc[
            group["ground_truth_confirmed"].astype(bool), "qiskit_version"].tolist()
        out.append({
            "case_directory": case,
            "issue_number": best.get("issue_number", ""),
            "issue_id": best.get("issue_id", ""),
            "platform": best.get("platform", ""),
            "versions_tested": len(group),
            "valid_repair_versions": len(valid_versions),
            "ground_truth_versions": len(gt_versions),
            "buggy_ever_failed": bool((group["buggy_status"] == classify.FAIL).any()),
            "fixed_ever_passed": bool((group["fixed_status"] == classify.PASS).any()),
            "ever_evaluable": bool(
                (group["pair_classification"] != classify.NOT_EVALUABLE).any()),
            "best_qiskit_version": best.get("qiskit_version", ""),
            "best_pair_classification": best.get("pair_classification", ""),
            "best_buggy_status": best.get("buggy_status", ""),
            "best_fixed_status": best.get("fixed_status", ""),
            "behavioral_bug_reproduced": best.get("behavioral_bug_reproduced", "UNKNOWN"),
            "behavioral_fix_verified": best.get("behavioral_fix_verified", "UNKNOWN"),
            "ground_truth_confirmed": bool(best.get("ground_truth_confirmed", False)),
            "best_evidence": str(best.get("behavioral_evidence", ""))[:500],
            "notes": str(best.get("notes", ""))[:300],
        })
    return pd.DataFrame(out).sort_values("case_directory")


def build_pair_matrix(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    versions = [v for v in all_versions() if v in set(df["qiskit_version"])]
    index: dict[str, dict] = {}
    for rec in df.to_dict("records"):
        case = rec["case_directory"]
        row = index.setdefault(case, {
            "case_directory": case,
            "issue_number": rec.get("issue_number", ""),
            "issue_id": rec.get("issue_id", ""),
            "platform": rec.get("platform", ""),
        })
        v = rec["qiskit_version"]
        row[f"{v}_buggy"] = classify.SHORT.get(rec.get("buggy_status", ""), "")
        row[f"{v}_fixed"] = classify.SHORT.get(rec.get("fixed_status", ""), "")

    cols = ["issue_number", "issue_id", "platform", "case_directory"]
    for v in versions:
        cols += [f"{v}_buggy", f"{v}_fixed"]
    out = pd.DataFrame(list(index.values()))
    for c in cols:
        if c not in out.columns:
            out[c] = ""
    return out[cols].sort_values("case_directory")


def build_version_stats(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    rows = []
    for v in all_versions():
        g = df[df["qiskit_version"] == v]
        if g.empty:
            continue
        n = len(g)
        evaluable = int((g["pair_classification"] != classify.NOT_EVALUABLE).sum())
        vr = int((g["pair_classification"] == classify.VALID_REPAIR).sum())
        rows.append({
            "qiskit_version": v,
            "cases_executed": n,
            "evaluable": evaluable,
            "VALID_REPAIR": vr,
            "VALID_REPAIR_pct": round(100 * vr / n, 1) if n else 0.0,
            "BUG_NOT_REPRODUCED": int((g["pair_classification"] == classify.BUG_NOT_REPRODUCED).sum()),
            "FIX_NOT_WORKING": int((g["pair_classification"] == classify.FIX_NOT_WORKING).sum()),
            "REGRESSION": int((g["pair_classification"] == classify.REGRESSION).sum()),
            "NOT_EVALUABLE": int((g["pair_classification"] == classify.NOT_EVALUABLE).sum()),
            "ground_truth_confirmed": int(g["ground_truth_confirmed"].astype(bool).sum()),
            "buggy_PASS": int((g["buggy_status"] == classify.PASS).sum()),
            "buggy_FAIL": int((g["buggy_status"] == classify.FAIL).sum()),
            "fixed_PASS": int((g["fixed_status"] == classify.PASS).sum()),
            "fixed_FAIL": int((g["fixed_status"] == classify.FAIL).sum()),
        })
    return pd.DataFrame(rows)


def build_summary(df: pd.DataFrame, cases: pd.DataFrame) -> pd.DataFrame:
    total_cases = len(cases)
    total_exec = len(df)
    def pct(n, d):
        return round(100 * n / d, 1) if d else 0.0

    pc = df["pair_classification"].value_counts().to_dict() if not df.empty else {}
    gt_cases = int(cases["ground_truth_confirmed"].sum()) if total_cases else 0
    strict_cases = int((cases["valid_repair_versions"] > 0).sum()) if total_cases else 0

    rows = [
        ("total reconstructed pairs tested", total_cases, ""),
        ("total case-version executions", total_exec, ""),
        ("", "", ""),
        ("VALID_REPAIR (buggy FAIL + fixed PASS)", pc.get(classify.VALID_REPAIR, 0),
         f"{pct(pc.get(classify.VALID_REPAIR, 0), total_exec)}% of executions"),
        ("BUG_NOT_REPRODUCED", pc.get(classify.BUG_NOT_REPRODUCED, 0),
         f"{pct(pc.get(classify.BUG_NOT_REPRODUCED, 0), total_exec)}%"),
        ("FIX_NOT_WORKING", pc.get(classify.FIX_NOT_WORKING, 0),
         f"{pct(pc.get(classify.FIX_NOT_WORKING, 0), total_exec)}%"),
        ("REGRESSION", pc.get(classify.REGRESSION, 0),
         f"{pct(pc.get(classify.REGRESSION, 0), total_exec)}%"),
        ("NOT_EVALUABLE", pc.get(classify.NOT_EVALUABLE, 0),
         f"{pct(pc.get(classify.NOT_EVALUABLE, 0), total_exec)}%"),
        ("", "", ""),
        ("GROUND_TRUTH_CONFIRMED executions",
         int(df["ground_truth_confirmed"].astype(bool).sum()) if total_exec else 0,
         f"{pct(int(df['ground_truth_confirmed'].astype(bool).sum()) if total_exec else 0, total_exec)}%"),
        ("", "", ""),
        ("-- case level --", "", ""),
        ("cases with VALID_REPAIR in >= 1 version", strict_cases, f"{pct(strict_cases, total_cases)}%"),
        ("cases with VALID_REPAIR in exactly 1 version",
         int((cases["valid_repair_versions"] == 1).sum()) if total_cases else 0, ""),
        ("cases with VALID_REPAIR in multiple versions",
         int((cases["valid_repair_versions"] > 1).sum()) if total_cases else 0, ""),
        ("cases where buggy never reproduces",
         int((~cases["buggy_ever_failed"].astype(bool)).sum()) if total_cases else 0, ""),
        ("cases where fixed never passes",
         int((~cases["fixed_ever_passed"].astype(bool)).sum()) if total_cases else 0, ""),
        ("cases never evaluable",
         int((~cases["ever_evaluable"].astype(bool)).sum()) if total_cases else 0, ""),
        ("", "", ""),
        ("-- headline yields --", "", ""),
        ("ground-truth executable yield", f"{gt_cases} / {total_cases}",
         f"{pct(gt_cases, total_cases)}%"),
        ("strict exception-based yield (buggy FAIL + fixed PASS)",
         f"{strict_cases} / {total_cases}", f"{pct(strict_cases, total_cases)}%"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "detail"])


def _clip_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if out[col].dtype == object:
            out[col] = out[col].astype(str).str.slice(0, _EXCEL_CELL)
    return out


def write_workbook(df: pd.DataFrame, cases: pd.DataFrame) -> Path:
    matrix = build_pair_matrix(df)
    vstats = build_version_stats(df)
    summary = build_summary(df, cases)
    env_rows = pd.DataFrame(envs.status_table())

    confirmed = cases[cases["ground_truth_confirmed"].astype(bool)][[
        "issue_number", "issue_id", "platform", "case_directory",
        "best_qiskit_version", "best_buggy_status", "best_fixed_status",
        "best_pair_classification", "behavioral_bug_reproduced",
        "behavioral_fix_verified", "ground_truth_confirmed", "best_evidence", "notes",
    ]] if not cases.empty else pd.DataFrame()

    review = cases[~cases["ground_truth_confirmed"].astype(bool)] if not cases.empty else pd.DataFrame()

    with pd.ExcelWriter(config.EXCEL_WORKBOOK, engine="openpyxl") as xl:
        summary.to_excel(xl, sheet_name="Summary", index=False)
        if not vstats.empty:
            vstats.to_excel(xl, sheet_name="Summary", index=False,
                            startrow=len(summary) + 3)
        _clip_frame(matrix).to_excel(xl, sheet_name="Pair_Matrix", index=False)
        _clip_frame(df).to_excel(xl, sheet_name="Detailed_Results", index=False)
        _clip_frame(env_rows).to_excel(xl, sheet_name="Environment_Matrix", index=False)
        _clip_frame(confirmed).to_excel(xl, sheet_name="Confirmed_Ground_Truth", index=False)
        _clip_frame(review).to_excel(xl, sheet_name="Needs_Review", index=False)
    return config.EXCEL_WORKBOOK


def export_subset(versions: list[str], prefix: str, summary_name: str | None = None) -> dict:
    """Export only the named versions, leaving the full-matrix files untouched.

    Used to publish a completed slice of the matrix while the rest is still
    pending. Writes ``<prefix>.csv`` (one row per case-version) and
    ``summary_<...>.csv`` (one row per version).
    """
    df = _load_frame()
    df = df[df["qiskit_version"].isin(versions)].copy()
    if df.empty:
        print(f"no recorded results for versions {versions}")
        return {}

    detail_path = config.PROJECT_ROOT / f"{prefix}.csv"
    df.to_csv(detail_path, index=False, encoding="utf-8")

    rows = []
    for v in versions:
        g = df[df["qiskit_version"] == v]
        if g.empty:
            continue
        n = len(g)
        gt = int(g["ground_truth_confirmed"].astype(bool).sum())
        rows.append({
            "qiskit_version": v,
            "total_cases": n,
            "VALID_REPAIR": int((g["pair_classification"] == classify.VALID_REPAIR).sum()),
            "BUG_NOT_REPRODUCED": int((g["pair_classification"] == classify.BUG_NOT_REPRODUCED).sum()),
            "FIX_NOT_WORKING": int((g["pair_classification"] == classify.FIX_NOT_WORKING).sum()),
            "REGRESSION": int((g["pair_classification"] == classify.REGRESSION).sum()),
            "NOT_EVALUABLE": int((g["pair_classification"] == classify.NOT_EVALUABLE).sum()),
            "GROUND_TRUTH_CONFIRMED": gt,
            "ground_truth_confirmed_percentage": round(100 * gt / n, 1) if n else 0.0,
        })
    summary = pd.DataFrame(rows)
    summary_path = config.PROJECT_ROOT / (summary_name or f"summary_{prefix}.csv")
    summary.to_csv(summary_path, index=False, encoding="utf-8")

    print(f"detail  : {detail_path}  ({len(df)} rows)")
    print(f"summary : {summary_path}  ({len(summary)} versions)")
    print()
    print_overall(df, versions)
    return {"detail": str(detail_path), "summary": str(summary_path),
            "frame": df, "summary_frame": summary}


def print_overall(df: pd.DataFrame, versions: list[str],
                  total_cases: int = 556) -> None:
    """Corpus-level rollup across whichever versions are covered by ``df``."""
    confirmed = df["ground_truth_confirmed"].astype(bool)
    gt_cases = df.loc[confirmed, "case_directory"].nunique()
    vr = df["pair_classification"] == classify.VALID_REPAIR
    vr_cases = df.loc[vr, "case_directory"].nunique()
    resolved = set(df.loc[confirmed, "case_directory"]) | set(df.loc[vr, "case_directory"])
    env_err = int((df["buggy_status"] == classify.ENVIRONMENT_ERROR).sum()
                  + (df["fixed_status"] == classify.ENVIRONMENT_ERROR).sum())

    needs_review = 0
    report = config.PROJECT_ROOT / "reconstructed_cases" / "reconstruction_report.csv"
    if report.exists():
        rec = pd.read_csv(report)
        needs_review = int((rec["reconstruction_status"] == "NEEDS_REVIEW").sum())

    def pct(n: int) -> str:
        return f"{100 * n / total_cases:.1f}%" if total_cases else "0.0%"

    print(f"=== OVERALL across {len(versions)} version(s): {', '.join(versions)} ===")
    print(f"total unique cases                        : {total_cases}")
    print(f"cases GROUND_TRUTH_CONFIRMED in >=1 ver   : {gt_cases}   ({pct(gt_cases)})")
    print(f"cases VALID_REPAIR in >=1 version         : {vr_cases}   ({pct(vr_cases)})")
    print(f"cases still unresolved                    : {total_cases - len(resolved)}"
          f"   ({pct(total_cases - len(resolved))})")
    print(f"reconstruction NEEDS_REVIEW               : {needs_review}   ({pct(needs_review)})")
    print(f"ENVIRONMENT_ERROR program results         : {env_err} of {2 * len(df)} program runs")
    print(f"total case-version executions             : {len(df)}")


def export_all() -> dict:
    df = _load_frame()
    cases = build_case_summary(df)
    csv_path = write_csv(df)
    xlsx_path = write_workbook(df, cases)
    print(f"execution CSV : {csv_path}  ({len(df)} rows)")
    print(f"excel workbook: {xlsx_path}  ({len(cases)} cases)")
    return {"executions": len(df), "cases": len(cases),
            "csv": str(csv_path), "xlsx": str(xlsx_path)}
