"""Intent-based regression against unmodified MUT; defaults to sibling fixed.py."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

def load_target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(MUT)
    namespace["_stdout"] = output.getvalue()
    return namespace

from unittest.mock import patch
from qiskit.result import Result

class Regression(unittest.TestCase):
    def test_inverse_shadow_map_matches_every_actual_local_measurement(self):
        draws, outcomes = [], []
        randint = np.random.randint
        get_counts = Result.get_counts
        def record_draw(*args, **kwargs):
            value = randint(*args, **kwargs)
            draws.append(np.asarray(value).copy())
            return value
        def record_counts(result, *args, **kwargs):
            value = get_counts(result, *args, **kwargs)
            outcomes.append(dict(value))
            return value
        # Observation-only wrappers: all 300 quantum simulations execute normally.
        with patch.object(np.random, "randint", record_draw), patch.object(Result, "get_counts", record_counts):
            m = load_target()
        self.assertEqual(len(draws), 300)
        self.assertEqual(len(outcomes), 300)
        h = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
        rotations = [h, h @ np.diag([1, -1j]), np.eye(2)]
        expected = np.zeros((4, 4), complex)
        for bases, counts in zip(draws, outcomes):
            self.assertEqual(sum(counts.values()), 1)
            bits = next(iter(counts)).replace(" ", "")
            self.assertEqual(len(bits), 2)
            factors = []
            for q in (0, 1):
                b = int(bits[-1-q])
                projector = np.diag([1-b, b])
                u = rotations[int(bases[q])]
                factors.append(3 * u.conj().T @ projector @ u - np.eye(2))
            expected += np.kron(factors[1], factors[0])
        expected /= 300
        np.testing.assert_allclose(m["record_rho"], expected, atol=1e-12,
            err_msg="Each inverse-map factor must use its own qubit outcome in Qiskit little-endian order")
        self.assertAlmostEqual(np.trace(m["record_rho"]).real, 1.0, places=10)

if __name__ == "__main__":
    unittest.main()
