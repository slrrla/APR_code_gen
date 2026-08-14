import qiskit
from qiskit.test.mock import FakeArmonk

# FakeArmonk is a local mock backend with only 1 qubit
backend = FakeArmonk()

# Initialize two qubits and create Entanglement using Hadamard and CX/CNOT Gate
q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
