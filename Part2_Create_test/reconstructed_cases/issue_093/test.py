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

from unittest.mock import patch
import shlex

class Regression(unittest.TestCase):
    def test_notebook_repository_is_fetched_before_local_package_install(self):
        # Offline workflow inspection only: never run pip, git, shell or network.
        with patch("subprocess.run") as invoked:
            load_target()
        commands = [call.args[0] for call in invoked.call_args_list]
        texts = [" ".join(c) if isinstance(c, (list, tuple)) else c for c in commands]
        clones = [i for i, c in enumerate(texts) if "git clone" in c and
                  "github.com/qiskit-community/qiskit-textbook" in c]
        installs = [i for i, c in enumerate(texts) if "pip install" in c and
                    "./qiskit-textbook-src" in c and "git+" not in c]
        self.assertTrue(clones, "Fetch the repository containing the actual notebooks")
        self.assertTrue(installs, "Install the package from the cloned local source")
        self.assertLess(clones[0], installs[0])

if __name__ == "__main__":
    unittest.main()
