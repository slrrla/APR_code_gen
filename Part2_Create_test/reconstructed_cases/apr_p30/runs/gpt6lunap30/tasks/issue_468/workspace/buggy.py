from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.aqua.operators.legacy import MatrixOperator, commutator
from qiskit.aqua.operators import op_converter

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# Aqua's legacy commutator operates on its operator types, rather than
# directly on DensityMatrix state objects. Wrap their matrices as operators.
op0 = op_converter.to_weighted_pauli_operator(MatrixOperator(dm0.data))
op1 = op_converter.to_weighted_pauli_operator(MatrixOperator(dm1.data))
commutator(op0, op1)
