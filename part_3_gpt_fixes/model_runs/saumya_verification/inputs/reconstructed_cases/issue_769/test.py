"""Recognize standard gates without requiring one spelling of their names."""
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
    def assert_recognized(self, name):
        from qiskit.circuit import Gate
        from qiskit.circuit.library import standard_gates
        from qiskit.quantum_info import Operator
        ns = load_target()
        recognize = ns["get_qiskit_gate"]
        matrix = np.asarray(getattr(standard_gates, name)().to_matrix())
        result = recognize(matrix)
        self.assertIsNotNone(result, name)
        if isinstance(result, str):
            # X, x and XGate all identify the requested gate. Resolve names
            # through Qiskit's actual standard gates instead of changing MUT.
            aliases = {}
            from inspect import getmembers, isclass
            for class_name, gate_class in getmembers(standard_gates, isclass):
                try:
                    gate = gate_class()
                    Operator(gate)
                except Exception:
                    continue
                for alias in (class_name, class_name.removesuffix("Gate"), gate.name):
                    aliases[alias.casefold()] = gate
            self.assertIn(result.casefold(), aliases,
                          "Return a standard gate name, rather than the generic unitary label")
            result = aliases[result.casefold()]
        elif isinstance(result, type):
            result = result()
        self.assertIsInstance(result, Gate, "Return a standard gate name or gate")
        self.assertNotEqual(result.name, "unitary", "The generic unitary label does not identify the gate")
        actual = np.asarray(Operator(result).data)
        self.assertEqual(actual.shape, matrix.shape)
        np.testing.assert_allclose(actual, matrix, atol=1e-10)

    def test_pauli_x_example_and_multiple_known_gates(self):
        for name in ("IGate", "XGate", "YGate", "ZGate", "HGate", "SGate",
                     "SdgGate", "TGate", "TdgGate"):
            with self.subTest(gate=name):
                self.assert_recognized(name)

    def test_standard_two_qubit_gates(self):
        # The question concerns standard gates generally, not only 1-qubit ones.
        for name in ("CXGate", "SwapGate"):
            with self.subTest(gate=name):
                self.assert_recognized(name)

if __name__ == "__main__":
    unittest.main()

