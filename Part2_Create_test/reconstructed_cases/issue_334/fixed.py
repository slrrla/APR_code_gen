import qiskit as qk
from qiskit.opflow.primitive_ops import PauliOp

result = (PauliOp(qk.quantum_info.Pauli("X")) + 1j*PauliOp(qk.quantum_info.Pauli("Y"))).to_matrix()
print(result)
