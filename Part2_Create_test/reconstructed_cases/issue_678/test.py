# intent: The four-bit Fourier adder computes 2+15 modulo16, preserving register a.
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
    def test_exact_modular_sum(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns['qc'].remove_final_measurements(inplace=False)
        state = Statevector.from_instruction(circuit)
        # q7..q4 hold b+a=1; q3..q0 retain a=2.
        expected = np.zeros(256, dtype=complex)
        expected[int('00010010',2)] = 1
        self.assertTrue(state.equiv(Statevector(expected)), 'Expected |0001 0010>.')

if __name__ == "__main__":
    unittest.main(argv=[""])
