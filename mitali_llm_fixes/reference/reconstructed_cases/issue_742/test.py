"""Verify observable conversion and an actual EstimatorV2 job on local Aer.
The source uses no noise model; no noisy-fidelity claim is made.
"""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


class TestIntent(unittest.TestCase):
    def test_local_estimator_observable_and_expectation(self):
        from qiskit.quantum_info import Statevector
        ns = load_target()
        expected_op = np.array([[1,0,0,-2j],[0,0,0,0],[0,0,0,0],[2j,0,0,1]])
        np.testing.assert_allclose(ns["obs"].to_matrix(),expected_op,atol=1e-10)
        state = Statevector.from_instruction(ns["qc"])
        exact = complex(state.expectation_value(ns["O"]))
        self.assertAlmostEqual(exact.imag,0,places=10)
        self.assertAlmostEqual(exact.real,1-np.sqrt(3),places=10)
        values = np.asarray(ns["exp_vals"],dtype=float).reshape(-1)
        self.assertEqual(values.shape,(1,))
        self.assertTrue(np.isfinite(values).all())
        self.assertAlmostEqual(float(values[0]),exact.real,delta=0.2)
        self.assertTrue(ns["job"].done())

if __name__ == "__main__":
    unittest.main()

