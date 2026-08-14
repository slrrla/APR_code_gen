import qiskit as qk
from qiskit.opflow.primitive_ops import PauliOp

result = (PauliOp(qk.quantum_info.Pauli("X")) + PauliOp(qk.quantum_info.Pauli("iY"))).to_matrix()
print(result)
