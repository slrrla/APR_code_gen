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
    def test_half_adder_records_sum_zero_and_carry_one_for_one_plus_one(self):
        qc = load_target()["circuit"]
        self.assertEqual((qc.num_qubits, qc.num_clbits), (3, 2))
        state = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
        expected = np.zeros(8)
        expected[5] = 1  # q2=carry=1, q1=sum=0, preserved q0=1.
        np.testing.assert_allclose(state.data, expected, atol=1e-12)
        measurements = [(qc.qubits.index(item[1][0]), qc.clbits.index(item[2][0]))
                        for item in qc.data if item[0].name == "measure"]
        self.assertEqual(measurements, [(1,0), (2,1)])

if __name__ == "__main__":
    unittest.main()
