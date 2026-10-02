"""Apply the real four-qubit custom gate to q[1], a[0], a[1], a[2].

The example's unrelated four-control X is optional. The oracle checks the
custom gate's qubit order and the complete 32-by-32 operator independently.
"""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, random_unitary


CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))


class TestCustomGateAcrossRegisters(unittest.TestCase):
    def test_gate_and_qubit_order(self):
        generated = []

        def seeded_unitary(dims, seed=None):
            # A real Qiskit unitary, with only the example's randomness seeded.
            value = random_unitary(dims, seed=772 if seed is None else seed)
            generated.append(np.asarray(value.data))
            return value

        with patch("qiskit.quantum_info.random_unitary", seeded_unitary):
            with contextlib.redirect_stdout(io.StringIO()):
                namespace = runpy.run_path(MUT)

        gates = [matrix for matrix in generated if matrix.shape == (16, 16)]
        self.assertEqual(len(gates), 1, "the example must produce one four-qubit custom unitary")
        matrix = gates[0]
        np.testing.assert_allclose(matrix.conj().T @ matrix, np.eye(16), atol=1e-12)

        circuits = []
        seen = set()
        for value in namespace.values():
            if isinstance(value, QuantumCircuit) and value.num_qubits == 5 and id(value) not in seen:
                circuits.append(value)
                seen.add(id(value))
        self.assertTrue(circuits, "no five-qubit circuit was produced")

        # Qiskit is little endian: leaving q[0] untouched embeds U as U tensor I.
        custom = np.kron(matrix, np.eye(2))
        mcx = np.eye(32, dtype=complex)
        mcx[15, 15] = mcx[31, 31] = 0
        mcx[15, 31] = mcx[31, 15] = 1
        failures = []
        for circuit in circuits:
            try:
                registers = {register.name: register for register in circuit.qregs}
                self.assertIn("q", registers)
                self.assertIn("a", registers)
                self.assertEqual(len(registers["q"]), 2)
                self.assertEqual(len(registers["a"]), 3)
                intended = [registers["q"][1]] + list(registers["a"])
                self.assertEqual([circuit.qubits.index(qubit) for qubit in intended], [1, 2, 3, 4])
                expected = np.eye(32, dtype=complex)
                custom_count = mcx_count = 0
                for instruction, qubits, clbits in circuit.data:
                    if instruction.name == "barrier":
                        continue
                    self.assertFalse(clbits, "the custom gate must be a unitary operation")
                    indices = [circuit.qubits.index(qubit) for qubit in qubits]
                    actual_gate = Operator(instruction).data
                    if instruction.num_qubits == 4:
                        self.assertEqual(list(qubits), intended,
                                         "the custom gate must receive the merged q[1] + a[:] list in order")
                        np.testing.assert_allclose(actual_gate, matrix, atol=1e-12)
                        expected = custom @ expected
                        custom_count += 1
                    else:
                        self.assertEqual(indices, [0, 1, 2, 3, 4])
                        np.testing.assert_allclose(actual_gate, mcx, atol=1e-12)
                        expected = mcx @ expected
                        mcx_count += 1
                self.assertEqual(custom_count, 1, "the custom gate must be applied exactly once")
                self.assertLessEqual(mcx_count, 1, "only the optional example MCX may accompany the gate")
                np.testing.assert_allclose(Operator(circuit).data, expected, atol=1e-11)
                return
            except (AssertionError, ValueError) as error:
                failures.append(str(error))
        self.fail("No circuit implements the intended custom gate: " + "; ".join(failures))


if __name__ == "__main__":
    unittest.main()
