import qiskit
# FIX: FakeArmonk has only one qubit -> import FakeVigo, because the circuit requires a backend with at least two qubits.
from qiskit.test.mock import FakeVigo

# FIX: The one-qubit backend cannot run this circuit -> use FakeVigo, because its five-qubit coupling map supports the two-qubit circuit.
backend = FakeVigo()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
