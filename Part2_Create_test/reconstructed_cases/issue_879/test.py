# intent: The reduced state of qubits 3 and 5 is the maximally mixed two-qubit density matrix.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest
from unittest.mock import patch

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def load_target():
    """Observe actual printed objects and text without changing the program."""
    objects = []
    stream = io.StringIO()
    original_print = print

    def observe(*args, **kwargs):
        objects.extend(args)
        return original_print(*args, **kwargs)

    with contextlib.redirect_stdout(stream), patch("builtins.print", observe):
        namespace = runpy.run_path(MUT)
    return namespace, objects, stream.getvalue()


class Test(unittest.TestCase):
    def test_reduced_density_matrix_and_purity(self):
        import numpy as np
        from qiskit.quantum_info import DensityMatrix
        ns, _, _ = load_target()
        reduced = [v for v in ns.values() if isinstance(v, DensityMatrix) and v.data.shape == (4,4)]
        self.assertTrue(reduced, 'A 12-qubit pure state is not the two-qubit reduced density matrix.')
        np.testing.assert_allclose(reduced[-1].data, np.eye(4)/4, atol=1e-10)
        self.assertAlmostEqual(float(np.real(reduced[-1].purity())), 0.25, places=10)

if __name__ == "__main__":
    unittest.main(argv=[""])
