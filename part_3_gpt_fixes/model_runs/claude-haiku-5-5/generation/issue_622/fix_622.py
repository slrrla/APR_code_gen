import qiskit
# FIX: FakeArmonk has only 1 qubit but the circuit needs 2 -> replaced with the 5-qubit FakeVigo mock backend, because the coupling map must have at least as many qubits as the circuit.
from qiskit.test.mock import FakeVigo

# FIX: FakeArmonk (1 qubit) -> FakeVigo (5 qubits), because the 2-qubit circuit must fit on the backend.
backend = FakeVigo()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
