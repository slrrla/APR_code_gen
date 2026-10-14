import qiskit
# FIX: FakeArmonk has only one qubit -> use a multi-qubit fake backend, because the circuit requires two qubits
from qiskit.test.mock import FakeYorktown

# FIX: FakeArmonk cannot run a two-qubit circuit -> use FakeYorktown, because it provides multiple qubits
backend = FakeYorktown()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
