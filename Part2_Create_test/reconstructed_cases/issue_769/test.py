"""Recognize nonparameterized standard gates by exact matrices, not global phase."""
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
    def test_pauli_x_example_and_multiple_known_gates(self):
        from qiskit.circuit.library import standard_gates
        ns = load_target()
        recognize = ns["get_qiskit_gate"]
        self.assertEqual(recognize(np.array([[0,1],[1,0]])),"XGate")
        for name in ("IGate","XGate","YGate","ZGate","HGate","SGate","SdgGate","TGate","TdgGate","CXGate","SwapGate"):
            matrix = np.asarray(getattr(standard_gates,name)().to_matrix())
            result = recognize(matrix)
            self.assertIsNotNone(result,name)
            actual = np.asarray(getattr(standard_gates,result)().to_matrix())
            np.testing.assert_allclose(actual,matrix,atol=1e-10)
    def test_unknown_and_parameterized_gate_return_none(self):
        ns = load_target()
        angle = 0.12345
        matrix = np.array([[np.cos(angle/2),-np.sin(angle/2)],[np.sin(angle/2),np.cos(angle/2)]])
        self.assertIsNone(ns["get_qiskit_gate"](matrix))
        self.assertIsNone(ns["get_qiskit_gate"](np.eye(3)))

if __name__ == "__main__":
    unittest.main()

