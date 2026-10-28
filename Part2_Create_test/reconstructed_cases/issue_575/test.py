# intent: The one-qubit feature state has relative phase exp(2ix).
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
    def test_manual_relative_phase(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        expected = Statevector([1/np.sqrt(2), np.exp(2j)/np.sqrt(2)])
        self.assertTrue(Statevector(ns['manual_state']).equiv(expected),
                        'The phase difference must be 2 radians, allowing global phase.')
        self.assertTrue(Statevector(ns['qiskit_state']).equiv(expected))

if __name__ == "__main__":
    unittest.main(argv=[""])
