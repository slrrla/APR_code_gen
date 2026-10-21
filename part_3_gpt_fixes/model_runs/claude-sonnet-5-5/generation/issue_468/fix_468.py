from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
# FIX: removed the Aqua legacy commutator import -> no import, because qiskit.aqua is removed and its commutator does not accept DensityMatrix objects

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# FIX: called the removed Aqua commutator on DensityMatrix objects -> compute AB - BA from the .data arrays, because this is the definition of the commutator and works on plain matrices
dm0.data @ dm1.data - dm1.data @ dm0.data
