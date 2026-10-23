from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.aqua.operators.legacy import commutator

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# FIX: legacy Aqua commutator() does not accept DensityMatrix objects -> compute the matrix commutator [A, B] = AB - BA from the .data arrays, because that is the quantity the user wants
result = dm0.data @ dm1.data - dm1.data @ dm0.data
