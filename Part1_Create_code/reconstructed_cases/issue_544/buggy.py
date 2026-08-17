from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from qiskit.visualization import array_to_latex

# Build a small Clifford circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.x(1)

stabstate = StabilizerState(qc)

# Attempt to get the density matrix from the stabilizer state
# This only returns the circuit as an Operator, not the desired density matrix
rho = stabstate.to_operator()

array_to_latex(rho)
