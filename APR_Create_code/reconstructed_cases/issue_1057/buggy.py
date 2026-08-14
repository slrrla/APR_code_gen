from qiskit import QuantumCircuit

circ = QuantumCircuit(2, 2)
circ.rxx(theta=0.3, qubit1=0, qubit2=1)
