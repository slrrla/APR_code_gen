from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.aqua.operators.legacy import commutator, MatrixOperator, op_converter

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# commutator expects WeightedPauliOperator instances, not DensityMatrix objects
# this raises an error
op0 = op_converter.to_weighted_pauli_operator(MatrixOperator(matrix=dm0.data))
op1 = op_converter.to_weighted_pauli_operator(MatrixOperator(matrix=dm1.data))
commutator_result = commutator(op0, op1)
