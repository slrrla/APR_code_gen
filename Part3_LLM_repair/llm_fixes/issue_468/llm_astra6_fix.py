from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
# FIX: The legacy commutator requires Aqua operators -> import MatrixOperator, because it provides the required operator interface.
from qiskit.aqua.operators.legacy import commutator, MatrixOperator

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# FIX: DensityMatrix inputs are incompatible with the legacy commutator -> wrap their data in MatrixOperator, because it supports Aqua's operator arithmetic.
commutator(MatrixOperator(matrix=dm0.data), MatrixOperator(matrix=dm1.data))

