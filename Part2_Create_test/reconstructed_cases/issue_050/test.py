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

class Regression(unittest.TestCase):
    def test_reports_actual_resolved_simulation_method(self):
        m = load_target()
        result = m["simulation_run"].result()
        self.assertTrue(result.success)
        method = result.results[0].metadata["method"]
        self.assertIn(method, {"statevector", "density_matrix", "stabilizer", "extended_stabilizer",
                               "matrix_product_state", "unitary", "superop", "tensor_network"})
        self.assertEqual(m["_stdout"].strip(), method)

if __name__ == "__main__":
    unittest.main()
