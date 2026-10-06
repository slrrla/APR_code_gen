"""Intent: OpenQASM 2 conditional operations compare the whole classical register."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


from qiskit import QuantumCircuit, execute

class TestIntent(unittest.TestCase):
    def test_register_conditions_and_both_branches(self):
        ns = load_target()
        circuit = ns["circuit"]
        self.assertEqual((circuit.num_qubits,circuit.num_clbits), (5,1))
        conditioned = [(op,q) for op,q,c in circuit.data if op.name.lower()=="cx"]
        self.assertEqual(len(conditioned), 6)
        self.assertEqual([tuple(circuit.qubits.index(bit) for bit in q) for _,q in conditioned],
                         [(1,2),(2,1),(1,2),(3,4),(4,3),(3,4)])
        for op,_ in conditioned:
            self.assertEqual(op.condition, (circuit.cregs[0],1))
        self.assertEqual(set(ns["result"].get_counts()), {"1"})
        # Prefix X on q0 cancels the source's input X, exercising condition false.
        prefix = QuantumCircuit(5,1)
        prefix.x(0)
        zero_input = prefix.compose(circuit)
        for source, expected in [(circuit,"1"),(zero_input,"0")]:
            counts = execute(source, ns["backend"], shots=128, seed_simulator=917).result().get_counts()
            self.assertGreater(sum(counts.values()),0)
            self.assertEqual(set(counts), {expected})
            self.assertAlmostEqual(counts[expected]/sum(counts.values()),1.0,places=12)

if __name__ == "__main__":
    unittest.main()

