"""Check real configuration files in a disposable home.

The repair may choose its own variable names, valid default contents, and file
creation command. Both requested files must exist and user settings must survive.
"""
import ast
import configparser
import os
from pathlib import Path
import shlex
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

import subprocess
import sys
import tempfile

class TestIntent(unittest.TestCase):
    def check_configuration(self, existing_profile=False, existing_settings=False, existing_kernel=False):
        with tempfile.TemporaryDirectory(prefix="apr096_") as temporary:
            home = Path(temporary)
            profile = home/".ipython"/"profile_default"
            settings = home/".qiskit"/"settings.conf"
            kernel = profile/"ipython_kernel_config.py"
            kernel_before = b"c = get_config()\n# Preserve my kernel preferences.\n"
            if existing_profile or existing_kernel:
                profile.mkdir(parents=True)
            if existing_kernel:
                kernel.write_bytes(kernel_before)
            if existing_settings:
                settings.parent.mkdir()
                settings.write_text("[default]\ncircuit_drawer = text\n", encoding="utf-8")
            expected = settings.read_bytes() if existing_settings else None
            env = dict(os.environ)
            env.update(USERPROFILE=str(home), HOME=str(home), IPYTHONDIR=str(home/".ipython"),
                       PYTHONDONTWRITEBYTECODE="1")
            prefix = Path(sys.executable).parent
            # Resolve the CLI to this interpreter's real IPython module. A
            # stale or inaccessible ipython.exe on PATH is a harness dependency
            # problem; the actual arguments and generated files remain real.
            command_dir = home / "test_cli"
            command_dir.mkdir()
            if os.name == "nt":
                (command_dir/"ipython.cmd").write_text(
                    '@"' + sys.executable + '" -m IPython %*\r\n', encoding="utf-8")
            else:
                command = command_dir / "ipython"
                command.write_text('#!/bin/sh\nexec ' + shlex.quote(sys.executable) + ' -m IPython "$@"\n', encoding="utf-8")
                command.chmod(0o755)
            env["PATH"] = os.pathsep.join(map(str, (command_dir, prefix, prefix/"Scripts"))) + os.pathsep + env.get("PATH", "")
            process = subprocess.run([sys.executable,"-B","-X","utf8",str(Path(MUT).resolve())],
                cwd=home, env=env, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=30)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            self.assertTrue(settings.is_file(), "Missing .qiskit/settings.conf")
            self.assertTrue(kernel.is_file(), "Missing ipython_kernel_config.py\n" + process.stdout + process.stderr)
            with settings.open(encoding="utf-8") as source:
                configparser.ConfigParser().read_file(source)
            ast.parse(kernel.read_text(encoding="utf-8"))
            if existing_settings:
                self.assertEqual(settings.read_bytes(), expected)
            if existing_kernel:
                self.assertEqual(kernel.read_bytes(), kernel_before)

    def test_clean_home(self):
        self.check_configuration()

    def test_preserves_existing_qiskit_settings(self):
        self.check_configuration(existing_settings=True)

    def test_existing_profile_missing_kernel_config(self):
        self.check_configuration(existing_profile=True)

    def test_preserves_existing_kernel_configuration(self):
        self.check_configuration(existing_kernel=True)

if __name__ == "__main__":
    unittest.main()

