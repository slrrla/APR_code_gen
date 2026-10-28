# intent: The six-qubit EfficientSU2 inverse must undo the variational circuit.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import numpy as np
from qiskit.quantum_info import Operator

class Test(unittest.TestCase):
    def test_inverse_identity_for_nonzero_parameters(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        forward, inverse = ns['var_form'], ns['var_form_inv']
        self.assertEqual((forward.num_qubits, inverse.num_qubits), (6, 6))
        values = {p: (i + 1) / 19.0 for i, p in enumerate(forward.parameters)}
        bound = forward.assign_parameters(values)
        bound_inverse = inverse.assign_parameters(values)
        self.assertTrue(Operator(bound.compose(bound_inverse)).equiv(Operator(np.eye(64))))

if __name__ == "__main__":
    unittest.main(argv=[""])
