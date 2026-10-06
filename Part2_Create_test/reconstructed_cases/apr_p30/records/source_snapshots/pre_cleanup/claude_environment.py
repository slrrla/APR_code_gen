"""Monitored local Bash environment for the original mini-swe-agent workflow.

This is NOT an OS security sandbox. The command checks catch visible attempts
to read withheld inputs or use the network; dynamically constructed Python or
shell expressions can evade those checks. No host credentials are inherited.
Windows Job Objects control process lifetime, not filesystem/network access.
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import shlex
import signal
import subprocess
import time
from typing import Any, Iterable
import uuid

from adapter import runtime_environment

GIT_BASH = Path(r"C:\Program Files\Git\bin\bash.exe")
SENTINEL = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"
EXECUTION_BOUNDARY = "Monitored local process; heuristic command guards; NOT an OS security sandbox"


@dataclass
class BashEnvironmentConfig:
    cwd: str
    interpreter: str
    bash_executable: str
    timeout: float
    support_path: str | None
    audit_path: str
    env: dict[str, str] = field(default_factory=dict)

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _shell_path(path: Path) -> str:
    text = path.resolve().as_posix()
    if os.name == "nt" and re.match(r"^[A-Za-z]:/", text):
        return "/" + text[0].lower() + text[2:]
    return text


class _WindowsJob:
    """Kill-on-close job, assigned before any untrusted command reaches Bash."""

    def __init__(self) -> None:
        class BasicLimits(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64),
                        ("PerJobUserTimeLimit", ctypes.c_int64),
                        ("LimitFlags", wintypes.DWORD),
                        ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t),
                        ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t),
                        ("PriorityClass", wintypes.DWORD),
                        ("SchedulingClass", wintypes.DWORD)]

        class IOCounters(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint64) for name in
                        ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                         "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", BasicLimits), ("IoInfo", IOCounters),
                        ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.kernel.CreateJobObjectW.restype = wintypes.HANDLE
        self.kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                                       wintypes.DWORD]
        self.kernel.SetInformationJobObject.restype = wintypes.BOOL
        self.kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self.kernel.AssignProcessToJobObject.restype = wintypes.BOOL
        self.kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        self.kernel.TerminateJobObject.restype = wintypes.BOOL
        self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self.kernel.CloseHandle.restype = wintypes.BOOL
        self.handle = self.kernel.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.BasicLimitInformation.LimitFlags = 0x00002000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.kernel.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def assign(self, process: subprocess.Popen) -> None:
        if not self.kernel.AssignProcessToJobObject(self.handle, wintypes.HANDLE(int(process._handle))):
            raise ctypes.WinError(ctypes.get_last_error())

    def kill(self) -> None:
        if self.handle and not self.kernel.TerminateJobObject(self.handle, 124):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self) -> None:
        if self.handle:
            self.kernel.CloseHandle(self.handle)
            self.handle = None


class MonitoredBashEnvironment:
    """mini-swe Environment protocol, keeping the supplied Python version pinned.

    The caller must keep validators, reference solutions, API keys, and prior
    trajectories outside ``workspace``. Command audit files are also outside it.
    API calls belong in a separate broker; this object never receives API keys.
    """

    def __init__(self, workspace: Path | str, interpreter: Path | str, *,
                 support_path: Path | str | None = None, audit_path: Path | str | None = None,
                 forbidden_paths: Iterable[Path | str] = (), timeout: float = 120,
                 bash_executable: Path | str = GIT_BASH, max_output_chars: int = 1_000_000):
        self.workspace = Path(workspace).resolve()
        self.interpreter = Path(interpreter).resolve()
        self.bash = Path(bash_executable).resolve()
        self.support = Path(support_path).resolve() if support_path else None
        self.audit_path = Path(audit_path).resolve() if audit_path else self.workspace.parent / "command_audit"
        if not self.workspace.is_dir():
            raise FileNotFoundError("Workspace is not a directory")
        if not self.interpreter.is_file() or not self.bash.is_file():
            raise FileNotFoundError("The pinned interpreter and Bash executable must exist")
        if timeout <= 0 or max_output_chars < 1:
            raise ValueError("Timeout and output limit must be positive")
        if _inside(self.audit_path, self.workspace):
            raise ValueError("Command audit files must be outside the agent workspace")
        self.audit_path.mkdir(parents=True, exist_ok=True)
        self.max_output_chars = max_output_chars
        self.session_id = uuid.uuid4().hex
        self.commands: list[dict[str, Any]] = []
        self.forbidden_paths = tuple(Path(p).resolve() for p in forbidden_paths) + (self.audit_path,)
        prefix = self.interpreter.parent
        if prefix.name.lower() in {"scripts", "bin"}:
            prefix = prefix.parent
        self.read_roots = (prefix, self.bash.parent.parent) + ((self.support,) if self.support else ())
        self.shim_dir = self.workspace / ".agent-bin"
        self.shim_dir.mkdir(exist_ok=True)
        wrapper = "#!/bin/bash\nexec " + shlex.quote(_shell_path(self.interpreter)) + ' "$@"\n'
        for name in ("python", "python3"):
            shim = self.shim_dir / name
            shim.write_text(wrapper, encoding="utf-8", newline="\n")
            if os.name != "nt":
                shim.chmod(0o700)
        env = runtime_environment(self.interpreter, self.workspace, self.workspace / "buggy.py",
                                  str(self.support) if self.support else None)
        # runtime_environment intentionally supports validators too; replace its
        # inherited host PATH with the small runtime/dependency path set here.
        path_parts = [self.shim_dir, self.interpreter.parent, prefix / "Library/bin",
                      prefix / "Scripts", self.bash.parent.parent / "usr/bin", self.bash.parent]
        if os.name == "nt":
            systemroot = env.get("SYSTEMROOT") or env.get("WINDIR")
            if systemroot:
                path_parts.append(Path(systemroot) / "System32")
        else:
            path_parts.extend([Path("/usr/bin"), Path("/bin")])
        env["PATH"] = os.pathsep.join(str(p) for p in path_parts if p.is_dir())
        env.update(PY="python", PAGER="cat", MANPAGER="cat", TQDM_DISABLE="1",
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   PYTHONNOUSERSITE="1", BASH_ENV=os.devnull, ENV=os.devnull,
                   MSWEA_GLOBAL_CONFIG_DIR=str(self.workspace / ".agent-config"), MSWEA_SILENT_STARTUP="1")
        self.config = BashEnvironmentConfig(str(self.workspace), str(self.interpreter), str(self.bash),
                                            float(timeout), str(self.support) if self.support else None,
                                            str(self.audit_path), env)

    def _guard(self, command: str, cwd: Path) -> list[str]:
        """Heuristics, deliberately not described as complete shell validation."""
        reasons = []
        plain = command.lower()
        # Bash/Python escapes such as '\n' are not absolute /n paths. Only
        # normalize drive-prefixed Windows filenames before path extraction.
        plain = re.sub(r"[a-z]:[\\/][^\s'\"<>;|]+", lambda match: match.group().replace("\\", "/"), plain)
        names_plain = plain.replace("\\", "/")
        if not _inside(cwd, self.workspace):
            reasons.append("cwd must remain within the isolated workspace")
        if not command.strip() or "\x00" in command or len(command) > 100_000:
            reasons.append("command is empty, contains NUL, or exceeds the command-size limit")
        if re.search(r"(?:^|[\s/'\"])\.\.(?:[/\s'\"]|$)", names_plain):
            reasons.append("parent-directory traversal is withheld")
        if re.search(r"(?:^|[/\s'\"])(?:fixed\.py|original\.py|test\.py|validator|"
                     r"sessionlogs?|trajector(?:y|ies)|prior[_-]?runs?|runs)(?:[/\s'\"]|$)", names_plain):
            reasons.append("withheld tests, reference solutions, or prior runs are prohibited")
        if re.search(r"(?:^|[/\s'\"])(?:\.env|\.aws|\.ssh|\.codex|\.agent-bin|\.agent-config)"
                     r"(?:[/\s'\"]|$)", names_plain):
            reasons.append("credential/configuration and protected runtime files are prohibited")
        if re.search(r"\b(?:anthropic_api_key|openai_api_key|aws_secret_access_key|"
                     r"aws_access_key_id|claude_api_key)\b", plain):
            reasons.append("credential access is prohibited")
        if re.search(r"(?:^|[;|&\n(]|\bsudo\s)\s*(?:[\w]+=[^\s]+\s+)*(?:[/\w:.-]+/)?"
                     r"(?:curl|wget|ssh|scp|sftp|ncat|netcat|nc|telnet|ftp|ping|"
                     r"pip\d*|conda|mamba|npm|npx|poetry|qmcp)(?:\.exe)?(?:\s|$)", plain):
            reasons.append("network, package-management, or MCP commands are prohibited")
        if re.search(r"(?:^|\s)-m\s+(?:pip|ensurepip|http\.server)\b", plain):
            reasons.append("package changes and network servers are prohibited")
        if re.search(r"\b(?:git\s+(?:clone|fetch|pull|push|ls-remote)|uv\s+(?:pip|sync|add))\b", plain):
            reasons.append("network/package operations are prohibited")
        if re.search(r"\b(?:from|import)\s+(?:requests|urllib|http\.client|socket|"
                     r"httpx|aiohttp|ftplib|smtplib|anthropic|openai)\b", plain):
            reasons.append("visible network/API client use is prohibited")
        if re.search(r"(?:^|[;|&\n])\s*(?:[/\w:.-]+/)?(?:powershell|pwsh|cmd|wscript|cscript|"
                     r"bash|sh|zsh)(?:\.exe)?(?:\s|$)", plain):
            reasons.append("alternate shell commands are prohibited")
        if re.search(r"\b(?:rm\s+[^\n;]*-(?:[a-z]*r[a-z]*)|rmdir\s+[^\n;]*/s|"
                     r"shutil\.rmtree|remove-item\s+[^\n;]*-recurse)\b", plain):
            reasons.append("recursive deletion requires trusted host-side target verification")
        # Explicit absolute paths are allowed only for the workspace and installed
        # dependencies. Imports inside Python still see the host filesystem.
        quoted = list(re.finditer(r"(['\"])((?:[a-z]:/|/)[^\n]*?)\1", plain))
        unquoted = re.finditer(r"(?:^|[\s='\"(])([a-z]:/[^\s'\"<>;|)]+|/[^\s'\"<>;|)]+)", plain)
        paths = [match.group(2) for match in quoted]
        paths += [match.group(1) for match in unquoted if not any(
            quoted_match.start() <= match.start(1) < quoted_match.end() for quoted_match in quoted)]
        for token in paths:
            if token in {"/dev/null", "/dev/stdin", "/dev/stdout", "/dev/stderr"}:
                continue
            if os.name == "nt" and re.match(r"^/[a-z]/", token):
                token = token[1] + ":" + token[2:]
            elif os.name == "nt" and token.startswith("/"):
                token = str(self.bash.parent.parent / token.lstrip("/"))
            path = Path(token)
            if any(_inside(path, forbidden) for forbidden in self.forbidden_paths):
                reasons.append("explicit path addresses withheld inputs or audit logs")
            elif not _inside(path, self.workspace) and not any(_inside(path, root) for root in self.read_roots):
                reasons.append("explicit path is outside workspace and installed dependencies")
            elif not _inside(path, self.workspace) and re.search(
                    r"\b(?:rm|mv|cp|rmdir|chmod|chown|unlink|rename|replace|write_text|write_bytes)\b|"
                    r"(?:^|[^<])>(?!>)|>>|open\([^\n]*[, ]['\"](?:w|a|x)", plain):
                reasons.append("dependency paths are read-only in the command policy")
        for forbidden in self.forbidden_paths:
            variants = (forbidden.as_posix().lower(), _shell_path(forbidden).lower())
            if any(value in names_plain for value in variants):
                reasons.append("explicit access to withheld input or audit path is prohibited")
        return list(dict.fromkeys(reasons))

    def _audit(self, event: dict[str, Any]) -> None:
        with (self.audit_path / "commands.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _run(self, command: str, cwd: Path, timeout: float, record: dict[str, Any]) -> dict[str, Any]:
        stdout_path = self.audit_path / f"command_{self.session_id}_{record['id']:04d}.stdout.txt"
        process = None
        job = None
        try:
            if os.name == "nt":
                job = _WindowsJob()
            with stdout_path.open("wb") as stdout:
                process = subprocess.Popen([str(self.bash), "--noprofile", "--norc", "-s", "--"],
                                           cwd=cwd, env=self.config.env, stdin=subprocess.PIPE,
                                           stdout=stdout, stderr=subprocess.STDOUT, text=True,
                                           encoding="utf-8", errors="replace",
                                           start_new_session=os.name != "nt",
                                           creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0)
                record["pid"] = process.pid
                if job:
                    job.assign(process)  # Fail closed: no script has been sent yet.
                record["process_tree_control"] = "Windows kill-on-close Job Object" if job else "POSIX process group"
                self._audit({"event": "started", **record})
                try:
                    process.communicate(command + "\n", timeout=timeout)
                    result = {"output": "", "returncode": process.returncode, "exception_info": ""}
                except subprocess.TimeoutExpired:
                    if job:
                        job.kill()
                    else:
                        os.killpg(process.pid, signal.SIGKILL)
                    process.communicate(timeout=15)
                    result = {"output": "", "returncode": -1,
                              "exception_info": f"Command timed out after {timeout:g}s",
                              "extra": {"exception_type": "TimeoutExpired", "timed_out": True}}
        except Exception as error:
            result = {"output": "", "returncode": -1,
                      "exception_info": f"{type(error).__name__}: {error}",
                      "extra": {"exception_type": type(error).__name__}}
        finally:
            if job:
                job.close()  # Also kill background descendants after successful commands.
            elif process is not None:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if process is not None and process.poll() is None:
                process.kill()
                process.communicate(timeout=15)
        record["stdout_log"] = str(stdout_path)
        if stdout_path.is_file():
            with stdout_path.open("rb") as handle:
                size = stdout_path.stat().st_size
                if size <= self.max_output_chars:
                    data = handle.read()
                else:
                    half = self.max_output_chars // 2
                    first = handle.read(half)
                    handle.seek(max(0, size - half))
                    data = first + b"\n[output truncated; full command output retained in host audit]\n" + handle.read(half)
                    result.setdefault("extra", {})["output_truncated"] = True
            result["output"] = data.decode("utf-8", errors="replace")
        return result

    def execute(self, action: dict, cwd: str = "", *, timeout: float | None = None) -> dict[str, Any]:
        command = action.get("command", "") if isinstance(action, dict) else ""
        requested_cwd = Path(cwd) if cwd else self.workspace
        if not requested_cwd.is_absolute():
            requested_cwd = self.workspace / requested_cwd
        requested_cwd = requested_cwd.resolve()
        actual_timeout = self.config.timeout if timeout is None else min(float(timeout), self.config.timeout)
        record = {"id": len(self.commands) + 1, "session_id": self.session_id,
                  "time_utc": datetime.now(timezone.utc).isoformat(),
                  "command": command, "cwd": str(requested_cwd), "timeout": actual_timeout,
                  "execution_boundary": EXECUTION_BOUNDARY}
        self.commands.append(record)
        self._audit({"event": "attempt", **record})
        started = time.monotonic()
        reasons = self._guard(command, requested_cwd) if isinstance(command, str) else ["command must be a string"]
        if actual_timeout <= 0:
            reasons.append("timeout must be positive")
        if reasons:
            result = {"output": "Command rejected by monitored execution policy: " + "; ".join(reasons) + "\n",
                      "returncode": 126, "exception_info": "CommandPolicyRejected",
                      "extra": {"exception_type": "CommandPolicyRejected", "guard_reasons": reasons}}
            record.update(status="POLICY_REJECTED", guard_reasons=reasons)
        else:
            result = self._run(command, requested_cwd, actual_timeout, record)
            record["status"] = "TIMEOUT" if result.get("extra", {}).get("timed_out") else (
                "EXECUTED" if not result["exception_info"] else "ENVIRONMENT_ERROR")
        record.update(returncode=result["returncode"], exception_info=result["exception_info"],
                      seconds=round(time.monotonic() - started, 3))
        if self._is_finished(result):
            record["status"] = "SUBMITTED"
        self._audit({"event": "result", **record})
        self._check_finished(result)
        return result

    @staticmethod
    def _is_finished(output: dict) -> bool:
        lines = output.get("output", "").lstrip().splitlines(keepends=True)
        return bool(lines and lines[0].strip() == SENTINEL and output.get("returncode") == 0)

    def _check_finished(self, output: dict) -> None:
        if self._is_finished(output):
            from minisweagent.exceptions import Submitted
            lines = output["output"].lstrip().splitlines(keepends=True)
            submission = "".join(lines[1:])
            raise Submitted({"role": "exit", "content": submission,
                             "extra": {"exit_status": "Submitted", "submission": submission}})

    def get_template_vars(self, **kwargs: Any) -> dict[str, Any]:
        return self.config.model_dump() | platform.uname()._asdict() | self.config.env | {
            "execution_boundary": EXECUTION_BOUNDARY,
            "pinned_interpreter": str(self.interpreter),
        } | kwargs

    def serialize(self) -> dict[str, Any]:
        return {"info": {"config": {"environment": self.config.model_dump(),
                                     "environment_type": f"{self.__class__.__module__}.{self.__class__.__name__}"},
                         "execution_boundary": EXECUTION_BOUNDARY,
                         "os_security_sandbox": False},
                "environment_commands": self.commands}


ClaudeEnvironment = MonitoredBashEnvironment
