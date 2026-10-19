"""Run the recovery circuit on all eight basis inputs, including c[2]=1."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


class TestIntent(unittest.TestCase):
    def test_full_conditional_truth_table(self):
        from qiskit import QuantumCircuit, ClassicalRegister, execute
        ns = load_target()
        source = ns["qc"]
        circuits = []
        for basis in range(8):
            circuit = QuantumCircuit(*source.qregs, *source.cregs)
            for bit in range(3):
                if basis & (1<<bit):
                    circuit.x(bit)
            circuit.compose(source, inplace=True)
            final = ClassicalRegister(3, "audit")
            circuit.add_register(final)
            circuit.measure(circuit.qubits, final)
            circuits.append(circuit)
        result = execute(circuits, ns["backend"], shots=128, seed_simulator=917).result()
        self.assertTrue(result.success)
        for basis, circuit in enumerate(circuits):
            expected = basis ^ 3 if basis & 3 == 3 else basis
            counts = result.get_counts(circuit)
            self.assertEqual(sum(counts.values()), 128)
            observed = {int(key.split(" ")[0], 2) for key in counts}
            self.assertEqual(observed, {expected}, "Conditional AND failed for basis %03d" % basis)

if __name__ == "__main__":
    unittest.main()

