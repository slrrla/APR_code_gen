"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestEntropy(unittest.TestCase):
    def test_normalized_state_and_zero_pure_entropy(self):
        from qiskit.quantum_info import entropy
        m = load_target()
        c, s = np.cos(0.5), np.sin(0.5)
        expected = np.array([c, -s, s, c]) / np.sqrt(2)
        actual = np.asarray(m['outputstate6'])
        np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)
        self.assertAlmostEqual(float(np.vdot(actual, actual).real), 1, places=12)
        np.testing.assert_allclose(m['probability'], np.abs(expected)**2, atol=1e-12)
        self.assertTrue(m['outstatevector'].is_valid())
        self.assertAlmostEqual(entropy(m['outstatevector']), 0, places=12)

if __name__ == "__main__":
    unittest.main()

