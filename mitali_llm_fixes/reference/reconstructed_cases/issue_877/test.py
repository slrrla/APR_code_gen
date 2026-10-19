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
    def test_offline_large_backend_calibration_noise(self):
        m = target()
        self.assertEqual(m["backend"].configuration().n_qubits, 27)
        self.assertFalse(m["noise_model"].is_ideal())
        errors = m["noise_model"].to_dict()["errors"]
        self.assertTrue(any(e["type"] == "roerror" for e in errors))
        self.assertTrue(any(e["type"] == "qerror" for e in errors))

    def test_noise_model_runs_on_actual_local_aer(self):
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator
        m = target()
        backend = AerSimulator(noise_model=m["noise_model"])
        qc = QuantumCircuit(2,2)
        qc.h(0)
        qc.cx(0,1)
        qc.measure([0,1],[0,1])
        result = backend.run(transpile(qc,backend),shots=256,seed_simulator=427).result()
        self.assertTrue(result.success)
        self.assertEqual(sum(result.get_counts().values()), 256)

if __name__ == "__main__":
    unittest.main()

