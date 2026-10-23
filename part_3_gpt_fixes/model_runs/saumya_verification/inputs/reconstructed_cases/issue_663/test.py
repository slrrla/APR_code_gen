"""Check real 1024-shot measurements and the complete prepared state."""
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
    def test_measured_distribution(self):
        from qiskit.quantum_info import Statevector
        ns = load_target()
        self.assertTrue(ns["result_sim"].success)
        counts = ns["counts"]
        self.assertEqual(sum(counts.values()), 1024)
        self.assertEqual(set(counts), {"001", "011"})
        self.assertAlmostEqual(counts["001"]/1024, 0.5, delta=0.12)
        circuit = ns["input_circuit"]
        self.assertEqual(circuit.count_ops().get("measure",0), 3)
        state = Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
        expected = np.zeros(8, complex)
        expected[[1,3]] = 1/np.sqrt(2)
        np.testing.assert_allclose(state.data, expected, atol=1e-10)

if __name__ == "__main__":
    unittest.main()

