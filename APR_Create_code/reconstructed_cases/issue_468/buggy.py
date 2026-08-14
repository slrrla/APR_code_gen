from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.aqua.operators.legacy import commutator

circ0 = QuantumCircuit(1)
circ1 = QuantumCircuit(1)

circ0.x(0)
dm0 = DensityMatrix.from_instruction(circ0)

circ1.z(0)
dm1 = DensityMatrix.from_instruction(circ1)

# commutator expects WeightedPauliOperator instances, not DensityMatrix objects
# this raises an error
commutator(dm0, dm1)
