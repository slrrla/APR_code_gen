"""mini-swe-agent environments for Qiskit repair.

Every action is a bash command. Commands that start with `qmcp` never reach the
shell: they are routed to the host-side MCP bridge, so MCP servers need not be
installed in the (py3.8 / py3.11) Qiskit sandboxes.

    qmcp list                          -> servers and their tools
    qmcp <server> <tool> '<json args>' -> call a tool, e.g.
    qmcp docs search_docs_tool '{"query": "execute removed qiskit 1.0"}'
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from typing import Any

from minisweagent.environments.docker import DockerEnvironment
from minisweagent.environments.local import LocalEnvironment, LocalEnvironmentConfig

from apr.mcp_bridge import MCPBridge

GIT_BASH = os.getenv("APR_BASH", r"C:\Program Files\Git\bin\bash.exe")

QMCP_USAGE = (
    "usage: qmcp list | qmcp <server> <tool> '<json args>'\n"
    "qmcp must be the whole command (no pipes, &&, or redirects)."
)


class MCPToolMixin:
    """Intercepts `qmcp ...` actions. Set `self.mcp = None` to disable MCP (ablation)."""

    mcp: MCPBridge | None = None
    mcp_calls: list[dict]

    def execute(self, action: dict, cwd: str = "", *, timeout: int | None = None) -> dict[str, Any]:
        command = action.get("command", "").strip()
        if command == "qmcp" or command.startswith("qmcp "):
            return self._qmcp(command)
        return super().execute(action, cwd, timeout=timeout)

    def _qmcp(self, command: str) -> dict[str, Any]:
        if self.mcp is None:
            return {"output": "bash: qmcp: command not found\n", "returncode": 127, "exception_info": ""}
        try:
            argv = shlex.split(command)[1:]
        except ValueError as e:
            return {"output": f"qmcp: {e}\n{QMCP_USAGE}\n", "returncode": 2, "exception_info": ""}
        try:
            if not argv or argv[0] in ("-h", "--help", "help"):
                out, rc = QMCP_USAGE, 0
            elif argv[0] == "list":
                lines = []
                for server in self.mcp.servers:
                    lines.append(f"[{server}]")
                    lines += [f"  {t['name']}({', '.join(t['args'])}): {t['description']}" for t in self.mcp.list_tools(server)]
                out, rc = "\n".join(lines), 0
            elif len(argv) in (2, 3):
                args = json.loads(argv[2]) if len(argv) == 3 else {}
                if not isinstance(args, dict):
                    raise ValueError("json args must be an object")
                out, is_err = self.mcp.call(argv[0], argv[1], args)
                rc = 1 if is_err else 0
            else:
                out, rc = QMCP_USAGE, 2
        except Exception as e:  # bad JSON, unknown server/tool, server crash
            out, rc = f"qmcp error: {type(e).__name__}: {e}\n{QMCP_USAGE}", 1
        self.mcp_calls.append({"command": command, "returncode": rc, "chars": len(out)})
        return {"output": out + "\n", "returncode": rc, "exception_info": ""}


class QiskitDockerEnv(MCPToolMixin, DockerEnvironment):
    """Runs bash inside a qiskit-apr:<modern|legacy> container with the task workspace at /work."""

    def __init__(self, *, mcp: MCPBridge | None, **kwargs):
        self.mcp = mcp
        self.mcp_calls = []
        super().__init__(**kwargs)

    def cleanup(self):
        # Upstream cleanup uses a POSIX shell one-liner, which cmd.exe cannot run.
        if getattr(self, "container_id", None):
            subprocess.Popen(
                [self.config.executable, "rm", "-f", self.container_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.container_id = None


class GitBashLocalEnv(MCPToolMixin, LocalEnvironment):
    """No-Docker fallback for quick iteration on Windows: Git Bash in a host directory.

    Not sandboxed and has network access, so the agent could in principle look up
    the original answer. Use Docker for reported numbers.
    """

    def __init__(self, *, mcp: MCPBridge | None, **kwargs):
        self.mcp = mcp
        self.mcp_calls = []
        super().__init__(config_class=LocalEnvironmentConfig, **kwargs)

    def execute(self, action: dict, cwd: str = "", *, timeout: int | None = None) -> dict[str, Any]:
        command = action.get("command", "").strip()
        if command == "qmcp" or command.startswith("qmcp "):
            return self._qmcp(command)
        cwd = cwd or self.config.cwd
        try:
            result = subprocess.run(
                [GIT_BASH, "-c", command],
                cwd=cwd,
                env=os.environ | self.config.env,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout or self.config.timeout,
            )
            output = {"output": result.stdout, "returncode": result.returncode, "exception_info": ""}
        except subprocess.TimeoutExpired as e:
            raw = e.output.decode("utf-8", "replace") if isinstance(e.output, bytes) else (e.output or "")
            output = {
                "output": raw,
                "returncode": -1,
                "exception_info": f"Command timed out after {e.timeout}s",
                "extra": {"exception_type": "TimeoutExpired", "exception": str(e)},
            }
        self._check_finished(output)
        return output
