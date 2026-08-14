"""Execute every reconstructed pair against every built Qiskit environment.

Roughly 556 cases x 29 releases x 2 programs, so the design is dominated by
three requirements: nothing may hang the corpus, nothing may be executed twice,
and no single failure may stop the run.

* every program runs in its own subprocess under a hard wall-clock timeout
* every (case, version) result is appended to a JSONL checkpoint as soon as it
  is known, so an interrupted run resumes exactly where it stopped
* each execution gets its own deterministic working directory, so programs that
  write files cannot see each other's output
* sockets are disabled inside the child before the program loads, so no case can
  reach IBM Quantum even if it tries
"""
from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import classify, config, envs
from .versions import get

# Installed into every working directory; disables the network before the
# target module is imported.
_SHIM = r'''
import sys, os, runpy, traceback
import socket

def _denied(*a, **k):
    raise OSError("network access is disabled in the qiskit test matrix")

class _DeadSocket(socket.socket):
    def __init__(self, *a, **k):
        raise OSError("network access is disabled in the qiskit test matrix")

socket.socket = _DeadSocket
socket.create_connection = _denied
socket.getaddrinfo = _denied
socket.gethostbyname = _denied
try:
    import ssl
    ssl.wrap_socket = _denied
except Exception:
    pass

try:
    import matplotlib
    matplotlib.use("Agg", force=True)
except Exception:
    pass

target = sys.argv[1]
try:
    runpy.run_path(target, run_name="__main__")
except SystemExit as exc:
    if exc.code not in (0, None):
        sys.stderr.write("\nMATRIX_EXC_TYPE=SystemExit\n")
        sys.exit(1)
except BaseException as exc:
    traceback.print_exc()
    sys.stderr.write("\nMATRIX_EXC_TYPE=%s\n" % type(exc).__name__)
    sys.exit(1)
'''


@dataclass
class ProgramRun:
    status: str = ""
    reason: str = ""
    exit_code: int | None = None
    runtime_seconds: float = 0.0
    stdout: str = ""
    stderr: str = ""


@dataclass
class MatrixResult:
    case_directory: str = ""
    issue_number: str = ""
    issue_id: str = ""
    platform: str = ""
    qiskit_version: str = ""
    python_version: str = ""
    buggy_status: str = ""
    buggy_exit_code: int | None = None
    buggy_runtime_seconds: float = 0.0
    buggy_stdout: str = ""
    buggy_stderr: str = ""
    buggy_reason: str = ""
    fixed_status: str = ""
    fixed_exit_code: int | None = None
    fixed_runtime_seconds: float = 0.0
    fixed_stdout: str = ""
    fixed_stderr: str = ""
    fixed_reason: str = ""
    behavioral_bug_reproduced: str = "UNKNOWN"
    behavioral_fix_verified: str = "UNKNOWN"
    behavioral_evidence: str = ""
    pair_classification: str = ""
    ground_truth_confirmed: bool = False
    notes: str = ""

    @property
    def key(self) -> str:
        return f"{self.case_directory}|{self.qiskit_version}"


def _clip(text: str) -> str:
    text = text or ""
    if len(text) <= config.MAX_CAPTURE_CHARS:
        return text
    keep = config.MAX_CAPTURE_CHARS
    return text[: keep // 2] + f"\n...[{len(text) - keep} chars elided]...\n" + text[-keep // 2:]


def wants_network(source: str) -> bool:
    return any(sym in source for sym in config.NETWORK_SYMBOLS)


# --------------------------------------------------------------------------
def run_program(python: Path, program: Path, workdir: Path,
                timeout: int) -> tuple[ProgramRun, bool, str]:
    """Run one program. Returns (result, timed_out, launch_error)."""
    workdir.mkdir(parents=True, exist_ok=True)
    shim = workdir / "_matrix_shim.py"
    shim.write_text(_SHIM, encoding="utf-8")

    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["QISKIT_SUPPRESS_PACKAGING_WARNINGS"] = "Y"
    for key in ("QISKIT_IBM_TOKEN", "QISKIT_IBM_CHANNEL", "QISKIT_IBM_INSTANCE",
                "IBMQ_TOKEN", "IBM_QUANTUM_TOKEN", "ANTHROPIC_API_KEY"):
        env.pop(key, None)

    run = ProgramRun()
    t0 = time.time()
    try:
        proc = subprocess.run(
            [str(python), str(shim), str(program.resolve())],
            cwd=str(workdir), env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        run.runtime_seconds = round(time.time() - t0, 2)
        run.stdout = _clip(exc.stdout.decode("utf-8", "replace")
                           if isinstance(exc.stdout, bytes) else (exc.stdout or ""))
        run.stderr = _clip(exc.stderr.decode("utf-8", "replace")
                           if isinstance(exc.stderr, bytes) else (exc.stderr or ""))
        return run, True, ""
    except (OSError, ValueError) as exc:
        run.runtime_seconds = round(time.time() - t0, 2)
        return run, False, f"{type(exc).__name__}: {exc}"

    run.runtime_seconds = round(time.time() - t0, 2)
    run.exit_code = proc.returncode
    run.stdout = _clip(proc.stdout)
    run.stderr = _clip(proc.stderr)
    return run, False, ""


def run_case_version(case_dir: Path, version: str, meta: dict,
                     oracle: dict | None, timeout: int) -> MatrixResult:
    spec = get(version)
    manifest = envs.load_manifest().get(version, {})
    env_ok = bool(manifest.get("ok"))

    res = MatrixResult(
        case_directory=case_dir.name,
        issue_number=str(meta.get("issue_number", "")),
        issue_id=str(meta.get("issue_id", "")),
        platform=str(meta.get("platform", "")),
        qiskit_version=version,
        python_version=manifest.get("python_actual") or spec.python,
    )

    buggy_path = case_dir / config.BUGGY_FILE
    fixed_path = case_dir / config.FIXED_FILE
    if not buggy_path.exists() or not fixed_path.exists():
        res.buggy_status = res.fixed_status = classify.NOT_TESTABLE
        res.buggy_reason = res.fixed_reason = "reconstructed artifacts missing"
        res.pair_classification = classify.NOT_EVALUABLE
        res.notes = "case has no buggy.py/fixed.py on disk"
        return res

    buggy_src = buggy_path.read_text(encoding="utf-8", errors="replace")
    fixed_src = fixed_path.read_text(encoding="utf-8", errors="replace")
    python = envs.env_python(spec)
    base = config.WORKDIR_ROOT / spec.env_name / case_dir.name

    for label, src, path in (("buggy", buggy_src, buggy_path), ("fixed", fixed_src, fixed_path)):
        net = wants_network(src)
        if env_ok and not net:
            run, timed_out, launch_err = run_program(python, path, base / label, timeout)
        else:
            run, timed_out, launch_err = ProgramRun(), False, ""
        status, reason = classify.classify_program(
            run.exit_code, run.stderr, timed_out, env_ok, net, launch_err)
        run.status, run.reason = status, reason
        setattr(res, f"{label}_status", status)
        setattr(res, f"{label}_reason", reason)
        setattr(res, f"{label}_exit_code", run.exit_code)
        setattr(res, f"{label}_runtime_seconds", run.runtime_seconds)
        setattr(res, f"{label}_stdout", run.stdout)
        setattr(res, f"{label}_stderr", run.stderr)

    res.pair_classification = classify.classify_pair(res.buggy_status, res.fixed_status)
    bug, fix, evidence = classify.evaluate_behaviour(
        oracle, res.buggy_stdout, res.fixed_stdout, res.buggy_status, res.fixed_status)
    res.behavioral_bug_reproduced = bug
    res.behavioral_fix_verified = fix
    res.behavioral_evidence = evidence[:600]
    res.ground_truth_confirmed = classify.ground_truth_confirmed(
        res.pair_classification, bug, fix)
    if not env_ok:
        res.notes = f"environment for qiskit {version} is not built"
    return res


# --------------------------------------------------------------------------
_lock = threading.Lock()


def load_results() -> dict[str, dict]:
    if not config.RESULTS_JSONL.exists():
        return {}
    out: dict[str, dict] = {}
    for line in config.RESULTS_JSONL.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        key = f"{rec.get('case_directory')}|{rec.get('qiskit_version')}"
        out[key] = rec
    return out


def append_result(res: MatrixResult) -> None:
    config.STATE_DIR.mkdir(parents=True, exist_ok=True)
    with _lock:
        with config.RESULTS_JSONL.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(res), ensure_ascii=False) + "\n")


def run_matrix(cases: list[Path], versions: list[str], meta_by_case: dict,
               oracles: dict, workers: int = None, timeout: int = None,
               force: bool = False, progress_every: int = 25) -> list[MatrixResult]:
    workers = workers or config.DEFAULT_WORKERS
    timeout = timeout or config.EXEC_TIMEOUT_SECONDS
    done = {} if force else load_results()

    todo = [(c, v) for v in versions for c in cases
            if force or f"{c.name}|{v}" not in done]
    total = len(cases) * len(versions)
    if len(todo) < total:
        print(f"resuming: {total - len(todo)} of {total} executions already recorded")
    if not todo:
        print("nothing to execute")
        return []

    print(f"executing {len(todo)} case/version pairs "
          f"({len(cases)} cases x {len(versions)} versions), workers={workers}, "
          f"timeout={timeout}s")

    results: list[MatrixResult] = []
    completed = 0
    t0 = time.time()

    def work(item):
        case, version = item
        try:
            return run_case_version(case, version, meta_by_case.get(case.name, {}),
                                    oracles.get(case.name), timeout)
        except Exception as exc:  # isolation: never let one pair kill the run
            r = MatrixResult(case_directory=case.name, qiskit_version=version)
            r.buggy_status = r.fixed_status = classify.ENVIRONMENT_ERROR
            r.pair_classification = classify.NOT_EVALUABLE
            r.notes = f"runner exception: {type(exc).__name__}: {exc}"[:400]
            return r

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(work, item): item for item in todo}
        for fut in as_completed(futures):
            res = fut.result()
            append_result(res)
            results.append(res)
            completed += 1
            if progress_every and completed % progress_every == 0:
                rate = completed / max(1e-6, time.time() - t0)
                eta = (len(todo) - completed) / max(1e-6, rate)
                print(f"  {completed}/{len(todo)}  ({rate:.1f}/s, eta {eta/60:.0f} min)",
                      flush=True)
    return results
