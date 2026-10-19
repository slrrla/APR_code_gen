"""Intent: compute <0|Z|0> with a local fake backend, without a Runtime account.
Remote SDK imports are rejected explicitly as an offline-contract assertion;
this is not a claim that a real authenticated Runtime job was executed.
The real local BackendEstimator is sampled with fixed seed and shot count.
"""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import builtins
import numpy as np
from qiskit.primitives import BackendEstimator
from qiskit.quantum_info import Statevector
from unittest.mock import patch

class TestIntent(unittest.TestCase):
    def test_local_fake_backend_estimation(self):
        actual_import = builtins.__import__
        def offline_import(name, *args, **kwargs):
            if name == "qiskit_ibm_runtime" or name.startswith("qiskit_ibm_runtime."):
                raise AssertionError("OFFLINE_CONTRACT: Runtime account/session is not a local fake backend")
            return actual_import(name, *args, **kwargs)
        original_run = BackendEstimator.run
        def seeded_run(estimator, *args, **kwargs):
            kwargs.setdefault("shots", 16384)
            kwargs.setdefault("seed_simulator", 917)
            return original_run(estimator, *args, **kwargs)
        with patch("builtins.__import__", side_effect=offline_import), patch.object(BackendEstimator,"run",seeded_run):
            ns = load_target()
        self.assertEqual(ns["qc"].num_qubits, 1)
        self.assertAlmostEqual(float(np.real(Statevector.from_instruction(ns["qc"]).expectation_value(ns["O"]))),1.0,places=12)
        values = np.asarray(ns["result"].values, dtype=float)
        self.assertEqual(values.shape,(1,))
        self.assertTrue(np.isfinite(values).all())
        self.assertGreaterEqual(values[0], -1)
        self.assertLessEqual(values[0], 1)
        # FakeNairobi includes readout noise, so its measured expectation is
        # near +1, not exactly +1. This conservative bound is not a golden sample.
        self.assertAlmostEqual(values[0],1.0,delta=0.2)

if __name__ == "__main__":
    unittest.main()

