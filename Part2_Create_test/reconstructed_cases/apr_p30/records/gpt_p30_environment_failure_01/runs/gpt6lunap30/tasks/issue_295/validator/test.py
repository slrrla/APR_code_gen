"""Intent: Deutsch's algorithm must distinguish both constant and both balanced oracles."""
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


import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

class TestIntent(unittest.TestCase):
    def test_all_four_boolean_oracles(self):
        ns = load_target()
        constant_one = QuantumCircuit(2)
        constant_one.x(1)
        balanced_not = QuantumCircuit(2)
        balanced_not.cx(0,1)
        balanced_not.x(1)
        inputs=[(ns["constant_oracle"](),0),(constant_one,0),
                (ns["balanced_oracle"](),1),(balanced_not,1)]
        for oracle,answer in inputs:
            with self.subTest(answer=answer,oracle=str(oracle.count_ops())):
                circuit=ns["deutsch_circuit"](oracle)
                self.assertEqual((circuit.num_qubits,circuit.num_clbits),(2,1))
                mapping=[(circuit.qubits.index(q[0]),circuit.clbits.index(c[0]))
                         for op,q,c in circuit.data if op.name=="measure"]
                self.assertEqual(mapping,[(0,0)])
                probabilities=Statevector.from_instruction(circuit.remove_final_measurements(inplace=False)).probabilities()
                expected=[1,0] if answer==0 else [0,1]
                np.testing.assert_allclose([sum(probabilities[::2]),sum(probabilities[1::2])],
                                           expected,atol=1e-12,rtol=0)

if __name__ == "__main__":
    unittest.main()

