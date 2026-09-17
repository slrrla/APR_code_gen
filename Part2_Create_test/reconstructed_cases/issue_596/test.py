"""Binding must preserve all four intended values and assemble a numeric circuit."""
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
class TestIntent(unittest.TestCase):
    def test_bound_circuit_semantics_and_qobj(self):
        from qiskit.quantum_info import Operator
        ns = load_target()
        qc = ns.get("bound_qc", ns["qc"])
        self.assertEqual(len(qc.parameters), 0)
        a, b = 0.1, 0.2+0.3+0.4
        rx = np.array([[np.cos(a/2), -1j*np.sin(a/2)], [-1j*np.sin(a/2), np.cos(a/2)]])
        ry = np.array([[np.cos(b/2), -np.sin(b/2)], [np.sin(b/2), np.cos(b/2)]])
        np.testing.assert_allclose(Operator(qc).data, np.kron(ry, rx), atol=1e-10)
        obj = ns["qobj"]
        self.assertEqual(obj.config.shots, 10)
        self.assertEqual(len(obj.experiments), 1)
        for instruction in obj.experiments[0].instructions:
            for value in getattr(instruction, "params", []):
                self.assertTrue(np.isfinite(complex(value)))

if __name__ == "__main__":
    unittest.main()

