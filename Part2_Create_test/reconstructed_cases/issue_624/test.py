"""Verify circuit-to-operator conversion and an actual local QAOA result.
No claim that this diagonal mixer finds the global ground state.
"""
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


import numpy as np
from unittest.mock import patch

class TestIntent(unittest.TestCase):
    def test_operator_conversion_and_qaoa_execution(self):
        from qiskit.algorithms import QAOA
        from qiskit.opflow import OperatorBase
        captured = []
        original = QAOA.compute_minimum_eigenvalue
        def observe(instance, operator, *args, **kwargs):
            result = original(instance, operator, *args, **kwargs)
            captured.append((operator, result))
            return result
        with patch.object(QAOA, "compute_minimum_eigenvalue", observe):
            ns = load_target()
        self.assertEqual(len(captured), 1)
        operator, result = captured[0]
        self.assertIsInstance(operator, OperatorBase)
        expected = np.diag([(-1)**bin(i).count("1") for i in range(16)])
        np.testing.assert_allclose(operator.to_matrix(), expected, atol=1e-10)
        self.assertEqual(operator.num_qubits, 4)
        value = complex(result.eigenvalue)
        self.assertAlmostEqual(value.imag, 0, places=8)
        self.assertLessEqual(abs(value.real), 1+1e-8)
        state_value = result.eigenstate
        state = np.asarray(state_value.to_matrix() if hasattr(state_value, "to_matrix") else state_value).reshape(-1)
        self.assertAlmostEqual(float(np.vdot(state, state).real), 1, places=8)
        self.assertAlmostEqual(float(np.vdot(state, expected@state).real), value.real, places=7)

if __name__ == "__main__":
    unittest.main()
