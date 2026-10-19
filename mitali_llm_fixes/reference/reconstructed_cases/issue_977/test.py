"""Regression tests against the unmodified MUT (default: sibling fixed.py)."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

@functools.lru_cache(None)
def target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))))
    namespace["_stdout"] = output.getvalue()
    return namespace

class Regression(unittest.TestCase):
    def test_dense_matrix_round_trip_and_pauli_coefficients(self):
        from itertools import product
        m=target()
        H=np.array([[4.07981221,-3.6713615,1.3943662,-1.05164319],
                    [-3.6713615,5.88262911,-4.14084507,1.37558685],
                    [1.3943662,-4.14084507,5.83098592,-3.54929577],
                    [-1.05164319,1.37558685,-3.54929577,3.79812207]])
        op=m["op"]
        self.assertEqual(op.num_qubits,2)
        np.testing.assert_allclose(op.to_matrix(),H,atol=1e-8)
        paulis={"I":np.eye(2),"X":np.array([[0,1],[1,0]]),
                "Y":np.array([[0,-1j],[1j,0]]),"Z":np.diag([1,-1])}
        coeff=dict(op.to_list())
        for a,b in product(paulis,repeat=2):
            expected=np.trace(np.kron(paulis[a],paulis[b]) @ H)/4
            self.assertAlmostEqual(abs(coeff.get(a+b,0)-expected),0,places=8)

if __name__ == "__main__":
    unittest.main()

