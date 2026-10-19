import qiskit
# FIX: FakeArmonk has only one qubit -> use a multi-qubit fake backend, because this circuit uses two qubits.
from qiskit.test.mock import FakeYorktown

# FIX: select a backend with at least two qubits -> use FakeYorktown, because FakeArmonk cannot run this circuit.
backend = FakeYorktown()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
