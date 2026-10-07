from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
# FIX: commutator requires Aqua OperatorBase inputs -> import MatrixOp, because DensityMatrix objects are not compatible
from qiskit.aqua.operators import MatrixOp
from qiskit.aqua.operators.legacy import commutator

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# FIX: DensityMatrix inputs are unsupported -> wrap their matrix data in MatrixOp, because commutator operates on Aqua operators
commutator(MatrixOp(dm0.data), MatrixOp(dm1.data))

