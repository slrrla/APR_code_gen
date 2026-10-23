# FIX: FakeArmonk has only one qubit -> import a multi-qubit backend, because the circuit uses two qubits
from qiskit.test.mock import FakeVigo

# FIX: the backend's one-qubit limit -> use FakeVigo, because it supports the two-qubit circuit
backend = FakeVigo()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)

