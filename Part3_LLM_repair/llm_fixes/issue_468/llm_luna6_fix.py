from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.aqua.operators.legacy import commutator
# FIX: DensityMatrix is not an opflow operator -> import MatrixOp to wrap its matrix data, because the legacy commutator operates on opflow operators
from qiskit.opflow import MatrixOp

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# FIX: commutator does not accept DensityMatrix objects -> wrap their matrices in MatrixOp, because it expects opflow operators
commutator(MatrixOp(dm0.data), MatrixOp(dm1.data))

