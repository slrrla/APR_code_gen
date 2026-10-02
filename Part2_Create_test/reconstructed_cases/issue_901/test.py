"""Check the H/S/CX example's output unitary and discrete gate basis.

Run with MUT=/path/to/program.py; the default is sibling fixed.py.
"""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest

import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Operator


@functools.lru_cache(None)
def target():
    with contextlib.redirect_stdout(io.StringIO()):
        namespace = runpy.run_path(
            os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))
        )
    # The examples expose their final circuit as discretized or qc_transpiled.
    # Accept other variable names by selecting the last circuit the program exposes.
    circuits = [value for value in namespace.values() if isinstance(value, QuantumCircuit)]
    if not circuits:
        raise AssertionError("The program must expose its output QuantumCircuit")
    return circuits[-1]


class Regression(unittest.TestCase):
    def test_output_uses_requested_discrete_basis(self):
        circuit = target()
        self.assertEqual(circuit.num_qubits, 2)
        self.assertEqual(circuit.num_clbits, 0)
        allowed = {"h", "t", "cx", "id"}
        unexpected = set(circuit.count_ops()) - allowed
        self.assertFalse(
            unexpected,
            "Output still contains gates outside {H, T, CNOT, I}: "
            + ", ".join(sorted(unexpected)),
        )

    def test_output_preserves_full_two_qubit_unitary(self):
        # Qiskit uses little-endian qubit indices: H(0) = I tensor H.
        h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        s = np.diag([1, 1j])
        cx = np.array(
            [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]],
            dtype=complex,
        )
        expected = cx @ np.kron(np.eye(2), s) @ np.kron(np.eye(2), h)
        actual = np.asarray(Operator(target()).data)
        self.assertEqual(actual.shape, (4, 4))
        # Compare every matrix element, allowing only physically irrelevant phase.
        overlap = np.vdot(expected, actual)
        self.assertGreater(abs(overlap), 1e-12)
        phase = overlap / abs(overlap)
        np.testing.assert_allclose(actual, phase * expected, atol=1e-8, rtol=0)


if __name__ == "__main__":
    unittest.main()
