"""Intent-based regression against unmodified MUT; defaults to sibling fixed.py."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

def load_target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(MUT)
    namespace["_stdout"] = output.getvalue()
    return namespace

from unittest.mock import patch

class Regression(unittest.TestCase):
    def test_observation_samples_both_branches_without_measuring_state(self):
        for random_value, expected_bit in ((0.25, 0), (0.75, 1)):
            with self.subTest(random_value=random_value), patch("random.random", return_value=random_value):
                m = load_target()
                self.assertNotIn("measure", m["qc"].count_ops())
                np.testing.assert_allclose(np.asarray(m["statevector"]),
                                           np.array([1,1])/np.sqrt(2), atol=1e-12)
                self.assertAlmostEqual(m["prob0"], 0.5, places=12)
                self.assertEqual(m["x"], expected_bit)

if __name__ == "__main__":
    unittest.main()
