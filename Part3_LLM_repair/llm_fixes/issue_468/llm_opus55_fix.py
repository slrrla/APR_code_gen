from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
# FIX: removed qiskit.aqua legacy commutator (removed module, only accepted WeightedPauliOperator) -> define commutator via quantum_info Operator, because it works directly on DensityMatrix/matrix inputs as [A,B]=AB-BA
from qiskit.quantum_info import Operator


def commutator(op_a, op_b):
    a = Operator(op_a)
    b = Operator(op_b)
    return a.dot(b) - b.dot(a)

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

commutator(dm0, dm1)
