from qiskit import QuantumCircuit

theta = 0.5
qc = QuantumCircuit(3)

# Implement e^{-i * theta * Z0 Z1 Z2} using a CNOT ladder around an RZ gate,
# since Qiskit has no built-in multi-qubit ZZ...Z rotation gate.
qc.cx(0, 2)
qc.cx(1, 2)
qc.rz(2 * theta, 2)
qc.cx(1, 2)
qc.cx(0, 2)

print(qc)
