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
    def test_full_register_barrier_separates_the_two_gate_layers(self):
        qc = load_target()["qp"]
        before, after, seen = [], [], False
        for item in qc.data:
            op, qargs = item[0], item[1]
            positions = tuple(qc.qubits.index(q) for q in qargs)
            if op.name == "barrier":
                self.assertEqual(set(positions), set(range(8)))
                seen = True
            elif op.name == "cx":
                (after if seen else before).append(positions)
            else:
                self.fail("Unexpected operation in the specified CNOT layers: " + op.name)
        self.assertTrue(seen, "A barrier must prevent scheduling across the two requested steps")
        self.assertEqual(before, [(0,1), (2,3), (4,5), (6,7)])
        self.assertEqual(after, [(1,2), (3,4), (5,6)])

if __name__ == "__main__":
    unittest.main()
