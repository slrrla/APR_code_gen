# intent: Prepare cos(theta/2)|0>+exp(i phi)sin(theta/2)|1>, up to global phase.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import numpy as np
from qiskit.quantum_info import Statevector

class Test(unittest.TestCase):
    def test_requested_arbitrary_state(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        expected = Statevector([np.cos(.25),np.exp(.3j)*np.sin(.25)])
        self.assertTrue(Statevector.from_instruction(ns['circuit']).equiv(expected))

if __name__ == "__main__":
    unittest.main(argv=[""])
