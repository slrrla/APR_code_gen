"""Intent: missing Qiskit and IPython configuration files are created.
All file operations and the real IPython subprocess use a disposable home.
Existing user configuration must be preserved. No Qiskit computation is involved.
"""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import subprocess
import sys
import tempfile
from unittest.mock import patch

class TestIntent(unittest.TestCase):
    def check_configuration(self, existing_profile=False, existing_settings=False):
        with tempfile.TemporaryDirectory(prefix="apr096_") as temporary:
            home = Path(temporary)
            profile = home/".ipython"/"profile_default"
            settings = home/".qiskit"/"settings.conf"
            if existing_profile:
                profile.mkdir(parents=True)
            if existing_settings:
                settings.parent.mkdir()
                settings.write_text("[default]\ncircuit_drawer = text\n", encoding="utf-8")
            expected = settings.read_text(encoding="utf-8") if existing_settings else "[default]\n"
            env = {"USERPROFILE":str(home), "HOME":str(home), "IPYTHONDIR":str(home/".ipython")}
            actual_expanduser = os.path.expanduser
            def expanduser(path):
                return str(home) if path == "~" else actual_expanduser(path)
            def system(command):
                self.assertEqual(command, "ipython profile create")
                # Execute the requested CLI with this test's interpreter, avoiding
                # an unrelated ipython executable on PATH.
                process = subprocess.run([sys.executable,"-m","IPython","profile","create"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                return process.returncode
            with patch.dict(os.environ,env), patch("os.path.expanduser",side_effect=expanduser), patch("os.system",side_effect=system):
                ns = load_target()
            self.assertEqual(settings.read_text(encoding="utf-8"), expected)
            self.assertEqual(ns["contents"], expected)
            self.assertTrue((profile/"ipython_kernel_config.py").is_file(),
                            "Missing ipython_kernel_config.py (even when the profile directory already exists)")

    def test_clean_home(self):
        self.check_configuration()

    def test_preserves_existing_qiskit_settings(self):
        self.check_configuration(existing_settings=True)

    def test_existing_profile_missing_kernel_config(self):
        self.check_configuration(existing_profile=True)

if __name__ == "__main__":
    unittest.main()

