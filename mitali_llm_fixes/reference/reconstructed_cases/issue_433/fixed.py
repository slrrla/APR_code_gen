import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit.extensions import CXGate, UnitaryGate, XGate


class CX:
    oneone: Operator = Operator(np.array([[0, 0], [0, 1]]))
    zerozero: Operator = Operator(np.array([[1, 0], [0, 0]]))

    def __cx_little_endian(self) -> UnitaryGate:
        return Operator(Pauli('I')).tensor(self.zerozero) + Operator(Pauli('X')).tensor(self.oneone)

    def __cx_big_endian(self) -> UnitaryGate:
        return self.zerozero.tensor(Operator(Pauli('I'))) + self.oneone.tensor(Operator(Pauli('X')))

    def is_cx(self, op_cx: Operator, is_little_endian=True) -> bool:
        return op_cx == self.cx(is_little_endian)

    def cx(self, is_little_endian=True) -> UnitaryGate:
        return self.__cx_little_endian() if is_little_endian else self.__cx_big_endian()


cx_obj: CX = CX()

# Use Operator's tensor product instead of numpy's kron, matching qubit ordering.
qc2 = QuantumCircuit(2)
qc2.append(cx_obj.cx(), [0, 1])
op_manual = Operator.from_circuit(qc2)
print(cx_obj.cx(True))
print(cx_obj.cx(False))
print(CXGate().to_matrix() == op_manual.data)

# Verify using a control gate and reverse_bits() to account for endianness.
cx_gate = XGate().control(1)
qc = QuantumCircuit(2)
qc.append(cx_gate, [0, 1])
print(cx_obj.is_cx(Operator.from_circuit(qc.reverse_bits()), is_little_endian=False))
