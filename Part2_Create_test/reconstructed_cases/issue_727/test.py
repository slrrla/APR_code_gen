"""Bind integer, fractional, negative and zero exponents to controlled phases."""
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
    def test_parameter_expression_and_bound_unitaries(self):
        from qiskit.quantum_info import Operator
        ns = load_target()
        circuit = ns["CROT_circ"]
        self.assertEqual(set(circuit.parameters),{ns["k"]})
        for exponent in (-1,0,0.5,1,2,3,8):
            with self.subTest(exponent=exponent):
                angle = 2*np.pi/(2**exponent)
                bound = circuit.assign_parameters({ns["k"]:exponent})
                self.assertEqual(len(bound.parameters),0)
                expected = np.diag([1,1,1,np.exp(1j*angle)])
                np.testing.assert_allclose(Operator(bound).data,expected,atol=1e-10)

if __name__ == "__main__":
    unittest.main()

