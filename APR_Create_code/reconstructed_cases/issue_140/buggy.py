from qiskit import QuantumCircuit

theta = 0.5
qc = QuantumCircuit(3)

# Attempting to directly implement the time evolution of a 3-qubit
# Pauli string Z0 Z1 Z2 that appears in the MAX-3-SAT clause Hamiltonian,
# by looking for an "RZZZ" gate analogous to RZZ used in MAX-CUT QAOA.
qc.rzzz(theta, 0, 1, 2)  # no such gate exists in Qiskit

print(qc)
