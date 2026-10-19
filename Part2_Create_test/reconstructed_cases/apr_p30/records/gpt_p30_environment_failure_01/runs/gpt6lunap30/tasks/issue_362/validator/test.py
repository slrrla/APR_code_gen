"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestSavedUnitary(unittest.TestCase):
    def test_saved_hadamard_unitary(self):
        m = load_target()
        expected = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        np.testing.assert_allclose(np.asarray(m['unitary']), expected, atol=1e-12)
        np.testing.assert_allclose(np.asarray(m['unitary']).conj().T @ np.asarray(m['unitary']), np.eye(2), atol=1e-12)
        self.assertEqual(m['circuit'].num_qubits, 1)
        result = m['job'].result() if hasattr(m['job'], 'result') else m['job']
        self.assertTrue(result.success)
        self.assertIn('unitary', result.data(0))

if __name__ == "__main__":
    unittest.main()

