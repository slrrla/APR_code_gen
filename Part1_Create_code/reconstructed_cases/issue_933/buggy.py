from qiskit.circuit import QuantumCircuit

circ = QuantumCircuit(4, 4)
# Gives error saying q_target needs to be a qubit
circ.mcry(q_controls=[0, 1], q_target=2, q_ancillae=None)
