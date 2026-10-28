"""Intent-based regression against unmodified MUT; defaults to sibling fixed.py."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

def load_target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(MUT)
    namespace["_stdout"] = output.getvalue()
    return namespace

import sys
from unittest.mock import patch

class Regression(unittest.TestCase):
    def test_install_command_targets_current_notebook_interpreter(self):
        # Offline command-construction test. Installation itself is never executed.
        with patch("subprocess.call", return_value=0) as invoked:
            load_target()
        commands = [call.args[0] for call in invoked.call_args_list]
        self.assertTrue(any(isinstance(c, (tuple, list)) and list(c[:4]) ==
                            [sys.executable, "-m", "pip", "install"] and "qiskit" in c[4:]
                            for c in commands), "Install into the running notebook kernel's interpreter")

if __name__ == "__main__":
    unittest.main()
