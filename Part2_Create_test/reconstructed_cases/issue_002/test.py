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
    def test_count_only_quantum_register_bits(self):
        m = load_target()
        self.assertEqual(m["qc"].num_qubits, 12)
        self.assertEqual(m["qc"].num_clbits, 2)
        self.assertEqual(m["num_qubits"], 12)
        self.assertEqual(m["_stdout"].strip(), "12")

if __name__ == "__main__":
    unittest.main()
