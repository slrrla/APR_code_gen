"""Turn valid_cases/ + the version-matrix CSVs into repair tasks.

A task is one (case, qiskit_version) pair where the buggy script fails and the
reference fix passes (`reproduced`). The agent sees the buggy script and its
traceback; fixed.py and url.txt stay hidden and are used only by the validator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

DATA_ROOT = Path(__file__).resolve().parents[2]  # .../APR2
CASES_DIR = DATA_ROOT / "valid_cases"
SUMMARY_CSV = DATA_ROOT / "qiskit_summary.csv"
MATRIX_CSV = DATA_ROOT / "qiskit_matrix.csv"
VALID_CSV = DATA_ROOT / "qiskit_valid_cases.csv"

LEGACY_PREFIX = "0.25."


def _vkey(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split("."))


def image_kind(version: str) -> str:
    return "legacy" if version.startswith(LEGACY_PREFIX) else "modern"


@dataclass
class Task:
    case: str
    qiskit_version: str
    title: str
    buggy_src: str
    fixed_src: str = field(repr=False)
    exception_type: str = ""
    exception_msg: str = ""
    stderr: str = field(default="", repr=False)

    @property
    def task_id(self) -> str:
        return f"{self.case}__qiskit-{self.qiskit_version}"

    @property
    def image_kind(self) -> str:
        return image_kind(self.qiskit_version)

    @property
    def error_text(self) -> str:
        tail = self.stderr.strip()
        if len(tail) > 4000:
            tail = "...\n" + tail[-4000:]
        return tail or f"{self.exception_type}: {self.exception_msg}"


def load_tasks(
    verdict: str = "reproduced",
    version_policy: str = "latest",
    cases: list[str] | None = None,
    versions: list[str] | None = None,
) -> list[Task]:
    """version_policy: 'latest' = newest version with the verdict per case, 'all' = every such version."""
    valid = set(pd.read_csv(VALID_CSV).case)
    summary = pd.read_csv(SUMMARY_CSV, dtype=str)
    summary = summary[summary.case.isin(valid) & (summary.verdict == verdict)]
    if cases:
        summary = summary[summary.case.isin(cases)]
    if versions:
        summary = summary[summary.qiskit_version.isin(versions)]

    pairs: list[tuple[str, str]] = []
    for case, grp in summary.groupby("case"):
        vs = sorted(grp.qiskit_version, key=_vkey)
        pairs += [(case, vs[-1])] if version_policy == "latest" else [(case, v) for v in vs]

    usecols = ["case", "variant", "qiskit_version", "exception_type", "exception_msg", "stderr", "title"]
    matrix = pd.read_csv(MATRIX_CSV, dtype=str, usecols=usecols, keep_default_na=False)
    matrix = matrix[matrix.variant == "buggy"].set_index(["case", "qiskit_version"])

    tasks = []
    for case, version in pairs:
        row = matrix.loc[(case, version)]
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]
        d = CASES_DIR / case
        tasks.append(
            Task(
                case=case,
                qiskit_version=version,
                title=row.title,
                buggy_src=(d / "buggy.py").read_text(encoding="utf-8"),
                fixed_src=(d / "fixed.py").read_text(encoding="utf-8"),
                exception_type=row.exception_type,
                exception_msg=row.exception_msg,
                stderr=row.stderr,
            )
        )
    return tasks


if __name__ == "__main__":
    ts = load_tasks()
    print(len(ts), "tasks")
    for t in ts[:5]:
        print(t.task_id, t.image_kind, "|", t.exception_type, t.exception_msg[:60])
