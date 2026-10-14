"""A two-qubit Bell circuit must complete on a sufficiently large local backend."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import numpy as np
class TestIntent(unittest.TestCase):
    def test_backend_capacity_and_bell_counts(self):
        from qiskit.quantum_info import Statevector
        ns = load_target()
        self.assertGreaterEqual(ns["backend"].configuration().n_qubits, 2)
        result = ns["job_exp"].result()
        self.assertTrue(result.success)
        counts = result.get_counts()
        self.assertEqual(sum(counts.values()), 1024)
        self.assertEqual(set(counts), {"00", "11"})
        self.assertLess(abs(counts["00"]/1024 - 0.5), 0.12)
        state = Statevector.from_instruction(ns["qc"].remove_final_measurements(inplace=False))
        np.testing.assert_allclose(state.data, np.array([1,0,0,1])/np.sqrt(2), atol=1e-10)

if __name__ == "__main__":
    unittest.main()

