"""Self-contained environment checks; never read an APR case or validator."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from claude_environment import GIT_BASH, SENTINEL, MonitoredBashEnvironment

ROOT = Path(__file__).resolve().parent


def process_running(pid: int) -> bool:
    if os.name == "nt":
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        try:
            code = wintypes.DWORD()
            return bool(kernel.GetExitCodeProcess(handle, ctypes.byref(code))) and code.value == 259
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    status = Path(f"/proc/{pid}/status")
    return not status.is_file() or "State:\tZ" not in status.read_text()


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="environment_unit_", dir=ROOT)
        self.root = Path(self.temporary.name).resolve()
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.config_dir = self.root / "global_config"
        self.config_dir.mkdir()
        self.env_patch = patch.dict(os.environ, {
            "MSWEA_GLOBAL_CONFIG_DIR": str(self.config_dir), "MSWEA_SILENT_STARTUP": "1",
            "ANTHROPIC_API_KEY": "unit-test-host-secret-never-in-child",
            "OPENAI_API_KEY": "unit-test-host-secret-never-in-child",
            "UNRELATED_HOST_SECRET": "unit-test-host-secret-never-in-child",
            "BASH_ENV": str(self.root / "should_never_be_sourced"),
        })
        self.env_patch.start()
        self.bash = GIT_BASH if os.name == "nt" else Path("/bin/bash")
        self.env = MonitoredBashEnvironment(self.workspace, sys.executable, timeout=5,
                                            bash_executable=self.bash, audit_path=self.root / "audit")

    def tearDown(self):
        self.env_patch.stop()
        self.temporary.cleanup()

    def test_pinned_python_and_sanitized_environment(self):
        result = self.env.execute({"command": "$PY - <<'PY'\nimport os, sys\nprint(sys.executable)\nprint('secret=' + str(any('unit-test-host-secret' in v for v in os.environ.values())))\nPY"})
        self.assertEqual(result["returncode"], 0, result)
        self.assertIn(str(Path(sys.executable).resolve()), result["output"])
        self.assertIn("secret=False", result["output"])
        self.assertNotIn("ANTHROPIC_API_KEY", self.env.get_template_vars())
        self.assertNotIn("unit-test-host-secret", json.dumps(self.env.serialize()["info"]["config"]))

    def test_edit_and_rerun_python_heredoc(self):
        result = self.env.execute({"command": "cat <<'EOF' > buggy.py\nimport math\nprint(math.sqrt(81))\nEOF\n$PY buggy.py"})
        self.assertEqual(result["returncode"], 0, result)
        self.assertEqual(result["output"].strip(), "9.0")
        self.assertTrue((self.workspace / "buggy.py").is_file())

    def test_subshell_cwd_and_environment_do_not_persist(self):
        (self.workspace / "subdirectory").mkdir()
        first = self.env.execute({"command": "cd subdirectory; export APR_TRANSIENT=value; pwd"})
        second = self.env.execute({"command": "printf '%s\\n' \"${APR_TRANSIENT-unset}\"; $PY -c 'import os; print(os.getcwd())'"})
        self.assertEqual(first["returncode"], 0)
        self.assertEqual(second["returncode"], 0)
        self.assertIn("unset", second["output"])
        self.assertIn(str(self.workspace), second["output"])

    def test_guard_rejections_are_logged_before_any_execution(self):
        commands = ["cat ../validator/test.py", "cat fixed.py", "cat /c/users/secret.txt",
                    "curl https://example.com", "$PY -m pip install x", "import socket",
                    "rm -rf .", "powershell -Command Get-Content", "cat .env", "ls runs"]
        for command in commands:
            with self.subTest(command=command):
                result = self.env.execute({"command": command})
                self.assertEqual(result["returncode"], 126, result)
                self.assertEqual(self.env.commands[-1]["status"], "POLICY_REJECTED")
                self.assertNotIn("pid", self.env.commands[-1])
        events = [json.loads(line) for line in (self.root / "audit/commands.jsonl").read_text().splitlines()]
        self.assertEqual(len(events), 2 * len(commands))
        self.assertTrue(all(e["event"] in {"attempt", "result"} for e in events))

    def test_dependency_introspection_is_allowed(self):
        result = self.env.execute({"command": "$PY - <<'PY'\nimport sys, inspect, json\nprint(json.dumps({'python': sys.version.split()[0], 'path': inspect.__file__}))\nPY"})
        self.assertEqual(result["returncode"], 0, result)
        self.assertIn("python", result["output"])

    def test_sed_and_printf_edit_paths_are_not_false_positives(self):
        commands = [
            r"sed -i 's/c.qasm()/qiskit.qasm2.dumps(c)/; s/^import qiskit\r$/import qiskit\r\nimport qiskit.qasm2\r/' buggy.py; cat buggy.py; $PY buggy.py",
            r"printf 'import qiskit\nimport qiskit.qasm2\n\nc = qiskit.QuantumCircuit(1)\nc.h(0)\n\nqasm_str = qiskit.qasm2.dumps(c)\nprint(qasm_str)\n' > buggy.py; $PY buggy.py",
            r"printf '\n'; $PY -c \"print('\\n')\"",
        ]
        for command in commands:
            self.assertEqual(self.env._guard(command, self.workspace), [], command)

    def test_windows_backslash_paths_and_traversal_are_rejected(self):
        for command in [r"cat C:\outside\answer.txt", r"cat ..\validator\test.py"]:
            self.assertTrue(self.env._guard(command, self.workspace), command)

    def test_quoted_dependency_path_with_spaces_is_allowed_for_read(self):
        path = self.bash.parent / "dependency filename with spaces.txt"
        self.assertEqual(self.env._guard("cat '" + path.as_posix() + "'", self.workspace), [])

    def test_external_and_symlink_cwd_are_rejected(self):
        result = self.env.execute({"command": "pwd"}, cwd=str(self.root))
        self.assertEqual(result["returncode"], 126)
        result = self.env.execute({"command": "pwd"}, cwd="..")
        self.assertEqual(result["returncode"], 126)

    def test_explicit_dependency_writes_are_rejected(self):
        interpreter = str(Path(sys.executable).resolve()).replace("\\", "/")
        result = self.env.execute({"command": f"rm '{interpreter}'"})
        self.assertEqual(result["returncode"], 126, result)
        result = self.env.execute({"command": f"printf x > '{interpreter}'"})
        self.assertEqual(result["returncode"], 126, result)

    def test_forbidden_custom_path_and_audit_are_rejected(self):
        forbidden = self.workspace / "withheld"
        self.env.forbidden_paths += (forbidden,)
        result = self.env.execute({"command": "cat '" + forbidden.as_posix() + "/answer.txt'"})
        self.assertEqual(result["returncode"], 126, result)
        result = self.env.execute({"command": "cat '" + self.env.audit_path.as_posix() + "/commands.jsonl'"})
        self.assertEqual(result["returncode"], 126, result)

    def test_timeout_kills_child_process_tree(self):
        result = self.env.execute({"command": "$PY - <<'PY'\nimport sys, subprocess, time\nchild = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\nprint(child.pid, flush=True)\ntime.sleep(60)\nPY"}, timeout=0.8)
        self.assertEqual(result["returncode"], -1, result)
        self.assertTrue(result.get("extra", {}).get("timed_out"), result)
        pid = int(result["output"].strip())
        deadline = time.monotonic() + 3
        while process_running(pid) and time.monotonic() < deadline:
            time.sleep(0.02)
        self.assertFalse(process_running(pid), "A command descendant survived timeout")
        self.assertEqual(self.env.commands[-1]["status"], "TIMEOUT")

    def test_successful_command_kills_background_descendants(self):
        result = self.env.execute({"command": "$PY - <<'PY'\nimport sys, subprocess\nchild = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\nprint(child.pid, flush=True)\nPY"})
        self.assertEqual(result["returncode"], 0, result)
        pid = int(result["output"].strip())
        deadline = time.monotonic() + 3
        while process_running(pid) and time.monotonic() < deadline:
            time.sleep(0.02)
        self.assertFalse(process_running(pid), "A command descendant survived job close")

    def test_exact_sentinel_and_failed_sentinel_behavior(self):
        from minisweagent.exceptions import Submitted
        result = self.env.execute({"command": "echo " + SENTINEL + "suffix"})
        self.assertEqual(result["returncode"], 0)
        result = self.env.execute({"command": "echo " + SENTINEL + "; exit 1"})
        self.assertEqual(result["returncode"], 1)
        with self.assertRaises(Submitted) as submitted:
            self.env.execute({"command": "echo " + SENTINEL})
        self.assertEqual(submitted.exception.messages[0]["extra"]["exit_status"], "Submitted")
        self.assertEqual(self.env.commands[-1]["status"], "SUBMITTED")

    def test_actual_default_agent_preserves_bash_workflow(self):
        from minisweagent.agents.default import DefaultAgent

        class ScriptedModel:
            def __init__(self):
                self.actions = iter(["$PY buggy.py", "cat <<'EOF' > buggy.py\nprint('repaired')\nEOF",
                                     "$PY buggy.py", "echo " + SENTINEL])

            def query(self, messages):
                return {"role": "assistant", "content": "", "extra": {
                    "actions": [{"command": next(self.actions)}], "cost": 0}}

            def format_message(self, **kwargs):
                return kwargs

            def format_observation_messages(self, message, outputs, template_vars=None):
                return [{"role": "user", "content": json.dumps(outputs)}]

            def get_template_vars(self, **kwargs):
                return kwargs

            def serialize(self):
                return {}

        (self.workspace / "buggy.py").write_text("raise ValueError('reproducible')\n")
        agent = DefaultAgent(ScriptedModel(), self.env, system_template="Use bash", instance_template="{{task}}",
                             step_limit=5, cost_limit=0, output_path=self.root / "trajectory.json")
        final = agent.run("repair the synthetic script")
        self.assertEqual(final["exit_status"], "Submitted")
        self.assertEqual(len(self.env.commands), 4)
        self.assertEqual(self.env.commands[0]["returncode"], 1)
        self.assertEqual(self.env.commands[2]["returncode"], 0)
        self.assertEqual(self.env.commands[3]["status"], "SUBMITTED")
        self.assertFalse(agent.serialize()["info"]["os_security_sandbox"])


if __name__ == "__main__":
    unittest.main()
