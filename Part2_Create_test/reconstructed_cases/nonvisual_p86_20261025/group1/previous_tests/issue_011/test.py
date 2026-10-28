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
    def test_shor_21_resources_and_controlled_modular_exponentiation(self):
        m = load_target()
        qc = m["qc"]
        self.assertEqual((qc.num_qubits, qc.num_clbits), (15, 10))
        # Five work qubits encode 0..20; ten controls resolve the period.
        stages = []
        for item in qc.data:
            op, qargs = item[0], item[1]
            positions = [qc.qubits.index(q) for q in qargs]
            if any(q >= 10 for q in positions) and len(positions) > 1:
                stages.append((op, positions))
        self.assertEqual(len(stages), 10)
        for k, (op, positions) in enumerate(stages):
            self.assertEqual(set(positions), set(range(10, 15)) | {k})
            actual = Operator(op).data
            expected = np.zeros((64, 64), complex)
            multiplier = pow(4, 2 ** k, 21)
            for control in (0, 1):
                for x in range(32):
                    y = multiplier * x % 21 if control and x < 21 else x
                    before = sum(((x >> j) & 1) << positions.index(10+j) for j in range(5))
                    before |= control << positions.index(k)
                    after = sum(((y >> j) & 1) << positions.index(10+j) for j in range(5))
                    after |= control << positions.index(k)
                    expected[after, before] = 1
            np.testing.assert_allclose(actual, expected, atol=1e-12)
        measurements = [(qc.qubits.index(item[1][0]), qc.clbits.index(item[2][0]))
                        for item in qc.data if item[0].name == "measure"]
        self.assertEqual(measurements, [(i, i) for i in range(10)])

if __name__ == "__main__":
    unittest.main()
