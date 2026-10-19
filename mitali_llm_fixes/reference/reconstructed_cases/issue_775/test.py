"""Parse OpenQASM into the intended Bell circuit and run the original backend.
The source contains no measurement, so no count-extraction claim is made.
"""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


class TestIntent(unittest.TestCase):
    def test_parsed_operator_and_original_job(self):
        from qiskit.quantum_info import Operator
        ns = load_target()
        circuit = ns["qc"]
        self.assertEqual((circuit.num_qubits,circuit.num_clbits),(2,2))
        self.assertEqual(dict(circuit.count_ops()),{"h":1,"cx":1})
        expected = np.array([[1,1,0,0],[0,0,1,-1],[0,0,1,1],[1,-1,0,0]])/np.sqrt(2)
        np.testing.assert_allclose(Operator(circuit).data,expected,atol=1e-10)
        self.assertTrue(ns["result"].success)
        self.assertEqual(len(ns["result"].results),1)

if __name__ == "__main__":
    unittest.main()

