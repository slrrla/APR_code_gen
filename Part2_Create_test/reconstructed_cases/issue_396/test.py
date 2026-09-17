"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestMultiTargetOracle(unittest.TestCase):
    def test_exact_marked_phases_and_grover_amplification(self):
        from qiskit.quantum_info import Operator, Statevector
        m = load_target()
        diagonal = np.ones(8); diagonal[[5,6]] = -1
        expected_oracle = np.diag(diagonal)
        np.testing.assert_allclose(Operator(m['oracle']).data, expected_oracle, atol=1e-12)
        expected_grover = (np.ones((8,8))/4 - np.eye(8)) @ expected_oracle
        np.testing.assert_allclose(Operator(m['grover_op']).data, expected_grover, atol=1e-12)
        amplified = Statevector(np.ones(8)/np.sqrt(8)).evolve(m['grover_op']).probabilities()
        expected = np.zeros(8); expected[[5,6]]=0.5
        np.testing.assert_allclose(amplified, expected, atol=1e-12)

if __name__ == "__main__":
    unittest.main()

