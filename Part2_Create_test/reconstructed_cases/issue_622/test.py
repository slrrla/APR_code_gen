"""A Bell circuit must execute on a backend with at least two qubits.

The reported bug is backend capacity. Both ideal simulators and noisy fake
devices are valid fixes; the question does not demand noiseless shot counts.
Check the prepared Bell state independently of the backend's measurement noise.
"""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
from numbers import Integral

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import numpy as np
class TestIntent(unittest.TestCase):
    def test_backend_capacity_and_bell_counts(self):
        from qiskit.quantum_info import Statevector, state_fidelity
        ns = load_target()
        backend = ns["backend"]
        capacity = getattr(backend, "num_qubits", None)
        if capacity is None:
            capacity = backend.configuration().n_qubits
        self.assertGreaterEqual(capacity, 2)
        result = ns["job_exp"].result()
        self.assertTrue(result.success)
        counts = result.get_counts()
        self.assertTrue(counts)
        self.assertTrue(set(counts).issubset({"00", "01", "10", "11"}))
        self.assertTrue(all(isinstance(n, Integral) and n >= 0 for n in counts.values()))
        self.assertEqual(sum(counts.values()), 1024)
        state = Statevector.from_instruction(ns["qc"].remove_final_measurements(inplace=False))
        ideal_bell = np.array([1,0,0,1])/np.sqrt(2)
        self.assertAlmostEqual(state_fidelity(state, ideal_bell), 1., places=10)

if __name__ == "__main__":
    unittest.main()

