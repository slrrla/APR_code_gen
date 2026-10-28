# intent: Implement the XY rotation with positive imaginary off-diagonal sine terms.
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
    def test_xy_operator_for_multiple_angles(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns['qc']
        parameters = list(circuit.parameters)
        self.assertEqual(len(parameters), 1)
        for angle in (0.0, np.pi/14, -0.7, np.pi):
            c, s = np.cos(angle/2), 1j*np.sin(angle/2)
            expected = Operator(np.array([[1,0,0,0],[0,c,s,0],[0,s,c,0],[0,0,0,1]]))
            bound = circuit.assign_parameters({parameters[0]: angle})
            self.assertTrue(Operator(bound).equiv(expected), 'Wrong XY operator at theta=' + str(angle))

if __name__ == "__main__":
    unittest.main(argv=[""])
