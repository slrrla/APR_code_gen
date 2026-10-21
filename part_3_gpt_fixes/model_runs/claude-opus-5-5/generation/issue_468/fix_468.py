from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
# FIX: aqua legacy commutator only accepts legacy Pauli operators (and aqua is removed) -> define commutator via quantum_info Operator, because it must compute AB - BA for matrix-like inputs such as DensityMatrix
from qiskit.quantum_info import Operator
def commutator(a, b):
    A = Operator(a.data)
    B = Operator(b.data)
    return A.dot(B) - B.dot(A)

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

commutator(dm0, dm1)
