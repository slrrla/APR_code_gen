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
    def test_reconstructed_hamiltonian_and_exact_evolution(self):
        from scipy.linalg import expm
        from qiskit.quantum_info import Operator
        m = target()
        I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1])
        # Independent dense oracle for the RECONSTRUCTED Z + XX model.
        H=(np.kron(np.kron(Z,I),I)+np.kron(np.kron(I,Z),I)+np.kron(np.kron(I,I),Z)
           +.5*(np.kron(np.kron(X,X),I)+np.kron(np.kron(I,X),X)+np.kron(np.kron(X,I),X)))
        np.testing.assert_allclose(m["H"].to_matrix(), H, atol=1e-10)
        np.testing.assert_allclose(Operator(m["circ"]).data, expm(-1j*H), atol=1e-9)
        self.assertEqual(m["circ"].num_qubits, 3)

if __name__ == "__main__":
    unittest.main()

