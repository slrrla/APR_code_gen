"""Bounded, offline execution of a reconstructed program.

Guarantees, in order of importance:

1. **No remote access.** Sockets are disabled inside the child before the
   target module is loaded, so no IBM Quantum backend, provider handshake or
   HTTP call can occur even if the program asks for one. Programs whose source
   obviously wants remote access are not executed at all.
2. **No hang.** Hard wall-clock timeout, and a non-interactive matplotlib
   backend so ``plt.show()`` cannot block.
3. **No side effects on the dataset.** The child runs in a scratch cwd.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import config

# Installed into the child before the target runs.
_RUNNER = r'''
import sys, os, runpy, traceback

# --- 1. hard-disable the network -------------------------------------------
import socket

def _denied(*args, **kwargs):
    raise OSError("network access is disabled in the reconstruction sandbox")

class _DeadSocket(socket.socket):
    def __init__(self, *a, **k):
        raise OSError("network access is disabled in the reconstruction sandbox")

socket.socket = _DeadSocket
socket.create_connection = _denied
socket.getaddrinfo = _denied
socket.gethostbyname = _denied
try:
    import ssl
    ssl.wrap_socket = _denied
except Exception:
    pass

# --- 2. never open a GUI window --------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg", force=True)
except Exception:
    pass

# --- 3. run the target ------------------------------------------------------
target = sys.argv[1]
try:
    runpy.run_path(target, run_name="__main__")
except SystemExit as exc:
    if exc.code not in (0, None):
        sys.stderr.write("SANDBOX_EXC_TYPE=SystemExit\n")
        sys.exit(1)
except BaseException as exc:
    sys.stderr.write("SANDBOX_EXC_TYPE=%s\n" % type(exc).__name__)
    traceback.print_exc()
    sys.exit(1)
'''


@dataclass
class ExecResult:
    status: str          # OK | ERROR | TIMEOUT | SKIPPED_NETWORK | SKIPPED_DISABLED | NO_FILE
    exc_type: str = ""
    stderr_tail: str = ""
    duration_s: float = 0.0

    @property
    def summary(self) -> str:
        if self.status == "ERROR" and self.exc_type:
            return f"ERROR:{self.exc_type}"
        return self.status


def wants_network(source: str) -> bool:
    return any(sym in source for sym in config.NETWORK_SYMBOLS)


def _extract_exc_type(stderr: str) -> str:
    for line in stderr.splitlines():
        if line.startswith("SANDBOX_EXC_TYPE="):
            return line.split("=", 1)[1].strip()
    # fall back to the last traceback line
    for line in reversed(stderr.strip().splitlines()):
        s = line.strip()
        if s and ":" in s and s[0].isalpha():
            head = s.split(":", 1)[0]
            if head.isidentifier():
                return head
    return ""


def run_file(path: Path, timeout: int | None = None) -> ExecResult:
    if not config.ENABLE_EXECUTION:
        return ExecResult("SKIPPED_DISABLED")
    if not path.exists():
        return ExecResult("NO_FILE")

    source = path.read_text(encoding="utf-8", errors="replace")
    if wants_network(source):
        return ExecResult("SKIPPED_NETWORK")

    timeout = timeout or config.EXEC_TIMEOUT_SECONDS
    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Make sure no stored IBM credentials can be picked up.
    for key in ("QISKIT_IBM_TOKEN", "QISKIT_IBM_CHANNEL", "QISKIT_IBM_INSTANCE",
                "IBMQ_TOKEN", "IBM_QUANTUM_TOKEN"):
        env.pop(key, None)

    with tempfile.TemporaryDirectory(prefix="apr_sandbox_") as tmp:
        runner = Path(tmp) / "_runner.py"
        runner.write_text(_RUNNER, encoding="utf-8")
        import time
        t0 = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, str(runner), str(path.resolve())],
                cwd=tmp,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return ExecResult("TIMEOUT", duration_s=round(time.time() - t0, 2))
        dur = round(time.time() - t0, 2)

    if proc.returncode == 0:
        return ExecResult("OK", duration_s=dur)
    stderr = proc.stderr or ""
    return ExecResult(
        "ERROR",
        exc_type=_extract_exc_type(stderr),
        stderr_tail=stderr.strip()[-600:],
        duration_s=dur,
    )
