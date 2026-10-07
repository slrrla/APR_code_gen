from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Pauli
from qiskit.aqua.operators.legacy import commutator, MatrixOperator
from qiskit.aqua.operators.legacy.op_converter import to_weighted_pauli_operator

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# commutator expects WeightedPauliOperator instances, so convert the matrices
op0 = to_weighted_pauli_operator(MatrixOperator(dm0.data))
op1 = to_weighted_pauli_operator(MatrixOperator(dm1.data))
print(commutator(op0, op1))
