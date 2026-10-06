"""Synchronous facade over long-lived MCP stdio sessions.

mini-swe-agent is synchronous and bash-only, so the harness keeps each MCP server
running in a background asyncio loop and exposes a blocking `call()` that the
environment uses when the agent issues a `qmcp ...` command.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import threading
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Only servers that work without IBM Quantum credentials. runtime/transpiler need
# QISKIT_IBM_TOKEN and talk to real hardware, which would make runs non-reproducible.
DEFAULT_SERVERS = {
    "docs": "qiskit-docs-mcp-server",
    "qiskit": "qiskit-mcp-server",
}

# get_page_tool accepts arbitrary URLs; keep the agent on the official docs so it
# cannot read the original Stack Exchange answer.
ALLOWED_URL_PREFIXES = ("https://quantum.cloud.ibm.com/", "http://quantum.cloud.ibm.com/")


def _resolve_exe(name: str) -> str:
    scripts = Path(sys.executable).parent
    exe = shutil.which(name, path=str(scripts)) or shutil.which(name)
    if not exe:
        raise FileNotFoundError(f"MCP server executable not found: {name}")
    return exe


class MCPBridge:
    def __init__(self, servers: dict[str, str] | None = None, *, timeout: float = 120, log_path: Path | None = None):
        self.servers = servers or DEFAULT_SERVERS
        self.timeout = timeout
        self._errlog = open(log_path, "a", encoding="utf-8") if log_path else open(os.devnull, "w")
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, name="mcp-bridge", daemon=True)
        self._thread.start()
        self._sessions: dict[str, ClientSession] = {}
        self._holders: dict[str, asyncio.Task] = {}
        self._stop: asyncio.Event | None = None
        self._open_lock = threading.Lock()

    # ---- lifecycle -------------------------------------------------------

    def _run(self, coro, timeout: float | None = None):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout or self.timeout)

    async def _open(self, name: str) -> None:
        if self._stop is None:
            self._stop = asyncio.Event()
        params = StdioServerParameters(
            command=_resolve_exe(self.servers[name]),
            args=[],
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        ready: asyncio.Future = self._loop.create_future()

        async def holder():
            try:
                async with stdio_client(params, errlog=self._errlog) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        ready.set_result(session)
                        await self._stop.wait()
            except BaseException as e:  # surface startup failures to the caller
                if not ready.done():
                    ready.set_exception(e)
                else:
                    raise

        self._holders[name] = asyncio.create_task(holder())
        self._sessions[name] = await ready

    def _session(self, name: str) -> ClientSession:
        if name not in self.servers:
            raise KeyError(f"unknown MCP server '{name}'. Available: {', '.join(self.servers)}")
        with self._open_lock:
            if name not in self._sessions:
                self._run(self._open(name), timeout=max(self.timeout, 180))
        return self._sessions[name]

    def close(self) -> None:
        if self._stop is not None:
            self._loop.call_soon_threadsafe(self._stop.set)
            try:
                self._run(asyncio.wait(list(self._holders.values()), timeout=10), timeout=15)
            except Exception:
                pass
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._errlog.close()

    # ---- tool calls ------------------------------------------------------

    def list_tools(self, name: str) -> list[dict[str, Any]]:
        session = self._session(name)
        result = self._run(session.list_tools())
        tools = []
        for t in result.tools:
            props = (t.inputSchema or {}).get("properties", {})
            required = set((t.inputSchema or {}).get("required", []))
            args = [f"{k}{'' if k in required else '?'}" for k in props]
            desc = (t.description or "").strip().splitlines()[0] if t.description else ""
            tools.append({"name": t.name, "args": args, "description": desc})
        return tools

    def call(self, name: str, tool: str, arguments: dict[str, Any]) -> tuple[str, bool]:
        """Returns (text, is_error)."""
        url = arguments.get("url")
        if isinstance(url, str) and "://" in url and not url.startswith(ALLOWED_URL_PREFIXES):
            return f"Blocked: only {ALLOWED_URL_PREFIXES[0]} URLs (or relative doc paths) are allowed.", True
        session = self._session(name)
        result = self._run(session.call_tool(tool, arguments))
        parts = []
        for block in result.content:
            text = getattr(block, "text", None)
            parts.append(text if text is not None else json.dumps(block.model_dump(mode="json")))
        if not parts and result.structuredContent is not None:
            parts.append(json.dumps(result.structuredContent, indent=2))
        return "\n".join(parts), bool(result.isError)


if __name__ == "__main__":
    # Smoke test: python -m apr.mcp_bridge
    bridge = MCPBridge()
    try:
        for server in bridge.servers:
            print(f"== {server}")
            for t in bridge.list_tools(server):
                print(f"  {t['name']}({', '.join(t['args'])}) - {t['description'][:80]}")
        text, err = bridge.call("docs", "search_docs_tool", {"query": "QuantumCircuit qasm removed", "top_k": 2})
        print("== search_docs_tool error=", err)
        print(text[:1500])
    finally:
        bridge.close()
