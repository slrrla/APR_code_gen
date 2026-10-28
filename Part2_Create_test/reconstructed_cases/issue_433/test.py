# intent: Construct the controlled-X matrix with q0 as control in little-endian order.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import numpy as np
from unittest.mock import patch
from qiskit.quantum_info import Operator

class Test(unittest.TestCase):
    def test_manual_controlled_x_action(self):
        observed = []
        original = Operator.from_circuit
        def observe(*args, **kwargs):
            result = original(*args, **kwargs)
            observed.append(result)
            return result
        with patch.object(Operator, 'from_circuit', side_effect=observe), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        manual = ns.get('op_manual', observed[-1] if observed else None)
        self.assertIsNotNone(manual, 'Expose the constructed controlled operator.')
        expected = np.array([[1,0,0,0], [0,0,0,1], [0,0,1,0], [0,1,0,0]], dtype=complex)
        self.assertTrue(Operator(manual).equiv(Operator(expected)), 'q0=1 flips q1: |01> maps to |11>.')

if __name__ == "__main__":
    unittest.main(argv=[""])
