"""Verify the unchanged 100000-shot GHZ experiment and exact state."""
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
    def test_ghz_measurements_and_state(self):
        from qiskit.quantum_info import Statevector
        ns = load_target()
        self.assertTrue(ns["result"].success)
        counts = ns["counts"]
        self.assertEqual(sum(counts.values()),100000)
        self.assertEqual(set(counts),{"000","111"})
        self.assertAlmostEqual(counts["000"]/100000,0.5,delta=0.02)
        self.assertEqual(ns["circ"].count_ops().get("measure",0),3)
        expected = np.zeros(8,complex)
        expected[[0,7]] = 1/np.sqrt(2)
        np.testing.assert_allclose(Statevector.from_instruction(ns["circ"].remove_final_measurements(inplace=False)).data,expected,atol=1e-10)

if __name__ == "__main__":
    unittest.main()

