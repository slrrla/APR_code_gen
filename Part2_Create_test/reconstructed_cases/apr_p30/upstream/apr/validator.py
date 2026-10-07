"""Independent re-execution of a candidate patch on the task's Qiskit version.

Labels:
  plausible  - patched script exits 0 on the target version
  suspicious - plausible, but looks like the error was hidden rather than fixed
               (new broad except, or most of the code deleted)
  output_match - stdout equals the reference fix's stdout (weak signal: sampling is random)
"""

from __future__ import annotations

import ast
import difflib
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from apr.dataset import Task

RUN_ENV = {
    "MPLBACKEND": "Agg",
    "PYTHONDONTWRITEBYTECODE": "1",
    "QISKIT_IN_PARALLEL": "FALSE",
    "OMP_NUM_THREADS": "1",
    "RAYON_NUM_THREADS": "1",
}
BROAD_EXCEPT = re.compile(r"^\s*except\s*(BaseException|Exception)?\s*(as\s+\w+)?\s*:", re.M)


@dataclass
class RunResult:
    status: str  # pass | fail | timeout
    returncode: int | None
    stdout: str
    stderr: str
    duration_s: float

    @property
    def last_error(self) -> str:
        lines = [l for l in self.stderr.strip().splitlines() if l.strip()]
        return lines[-1] if lines else ""


class Runner:
    """Executes a single script under a pinned Qiskit version."""

    def __init__(self, backend: str = "docker", *, timeout: int = 120, local_venvs: Path | None = None):
        self.backend = backend
        self.timeout = timeout
        self.local_venvs = local_venvs

    def run(self, source: str, version: str, image: str) -> RunResult:
        workdir = Path(tempfile.mkdtemp(prefix="apr_val_"))
        (workdir / "script.py").write_text(source, encoding="utf-8")
        if self.backend == "docker":
            cmd = ["docker", "run", "--rm", "--network", "none", "--memory", "8g",
                   "-v", f"{workdir}:/work", "-w", "/work"]
            for k, v in RUN_ENV.items():
                cmd += ["-e", f"{k}={v}"]
            cmd += [image, f"/opt/venvs/qiskit-{version}/bin/python", "script.py"]
            env = None
        else:
            py = self.local_venvs / f"qiskit-{version}" / "Scripts" / "python.exe"
            if not py.exists():
                raise FileNotFoundError(f"local venv for qiskit {version} not found: {py}")
            cmd = [str(py), "script.py"]
            env = os.environ | RUN_ENV | {"HOME": str(workdir), "MPLCONFIGDIR": str(workdir)}
        t0 = time.perf_counter()
        try:
            p = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=self.timeout)
            status = "pass" if p.returncode == 0 else "fail"
            res = RunResult(status, p.returncode, p.stdout, p.stderr, time.perf_counter() - t0)
        except subprocess.TimeoutExpired as e:
            res = RunResult("timeout", None, str(e.stdout or ""), str(e.stderr or ""), time.perf_counter() - t0)
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
        return res


@dataclass
class Verdict:
    plausible: bool
    suspicious: bool
    output_match: bool | None
    patched_status: str
    patched_error: str
    fixed_status: str
    diff_lines: int
    len_ratio: float
    syntax_ok: bool
    reasons: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _code_lines(src: str) -> list[str]:
    return [l for l in src.splitlines() if l.strip() and not l.strip().startswith("#")]


def unified_diff(before: str, after: str, name: str = "buggy.py") -> str:
    return "".join(difflib.unified_diff(
        before.splitlines(keepends=True), after.splitlines(keepends=True), f"a/{name}", f"b/{name}"))


def validate(task: Task, patched_src: str, runner: Runner, image: str) -> Verdict:
    reasons = []
    try:
        ast.parse(patched_src)
        syntax_ok = True
    except SyntaxError as e:
        syntax_ok = False
        reasons.append(f"syntax error: {e}")

    diff = unified_diff(task.buggy_src, patched_src)
    diff_lines = sum(1 for l in diff.splitlines() if l[:1] in "+-" and l[:3] not in ("+++", "---"))
    len_ratio = len(_code_lines(patched_src)) / max(1, len(_code_lines(task.buggy_src)))

    if diff_lines == 0:
        reasons.append("no change")
    added_broad = len(BROAD_EXCEPT.findall(patched_src)) > len(BROAD_EXCEPT.findall(task.buggy_src))
    if added_broad:
        reasons.append("adds broad except")
    if len_ratio < 0.3:
        reasons.append(f"deletes most code (len_ratio={len_ratio:.2f})")

    patched = runner.run(patched_src, task.qiskit_version, image)
    fixed = runner.run(task.fixed_src, task.qiskit_version, image)
    plausible = patched.status == "pass"
    output_match = (patched.stdout.strip() == fixed.stdout.strip()) if plausible and fixed.status == "pass" else None
    return Verdict(
        plausible=plausible,
        suspicious=plausible and (added_broad or len_ratio < 0.3 or diff_lines == 0),
        output_match=output_match,
        patched_status=patched.status,
        patched_error=patched.last_error,
        fixed_status=fixed.status,
        diff_lines=diff_lines,
        len_ratio=round(len_ratio, 3),
        syntax_ok=syntax_ok,
        reasons=reasons,
    )
