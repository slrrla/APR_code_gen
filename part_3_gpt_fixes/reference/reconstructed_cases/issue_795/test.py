"""Verify the converted gate's matrix, inverse, and coherent controlled action."""
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
    def test_unitary_gate_and_controlled_matrix(self):
        from qiskit.quantum_info import Operator
        from qiskit.circuit import Gate
        ns = load_target()
        gate = ns.get("gate",ns["circuit"].to_gate())
        self.assertIsInstance(gate,Gate)
        expected = np.array([[0.5,-np.sqrt(0.75)],[np.sqrt(0.75),0.5]])
        np.testing.assert_allclose(Operator(gate).data,expected,atol=1e-10)
        np.testing.assert_allclose(Operator(gate.inverse()).data,expected.T,atol=1e-10)
        controlled = np.eye(4,dtype=complex)
        controlled[np.ix_([1,3],[1,3])] = expected
        np.testing.assert_allclose(Operator(gate.control()).data,controlled,atol=1e-9)

if __name__ == "__main__":
    unittest.main()

