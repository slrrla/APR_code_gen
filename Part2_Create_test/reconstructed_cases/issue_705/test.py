# intent: Return U3 angles that reconstruct the requested nonidentity unitary.
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
    def test_angles_reconstruct_the_requested_matrix(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
            target = np.array([[np.sqrt(.2),np.sqrt(.8)],[-np.sqrt(.8),np.sqrt(.2)]],dtype=complex)
            if callable(ns.get('get_angles')):
                import sympy as sp
                solutions = ns['get_angles'](sp.sqrt(sp.Rational(1,5)),sp.sqrt(sp.Rational(4,5)),
                                             -sp.sqrt(sp.Rational(4,5)),sp.sqrt(sp.Rational(1,5)))
                triples = []
                for solution in solutions:
                    angles = {str(key).lstrip(chr(92)): float(value.evalf()) for key,value in solution.items()}
                    triples.append((angles['theta'],angles['phi'],angles['lambda']))
            else:
                triples = [(ns['theta'], ns['phi'], ns.get('lam',ns.get('lamb')))]
        self.assertTrue(triples, 'Return at least one valid angle solution.')
        for theta, phi, lam in triples:
            c,s = np.cos(theta/2),np.sin(theta/2)
            matrix = np.array([[c,-np.exp(1j*lam)*s],[np.exp(1j*phi)*s,np.exp(1j*(phi+lam))*c]])
            self.assertTrue(Operator(matrix).equiv(Operator(target)), 'U3 angles must reconstruct the requested matrix.')

if __name__ == "__main__":
    unittest.main(argv=[""])
