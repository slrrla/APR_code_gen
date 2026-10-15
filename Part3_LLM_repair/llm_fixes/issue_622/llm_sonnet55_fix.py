# FIX: FakeArmonk is a 1-qubit backend -> switch to FakeAthens (5 qubits), because the 2-qubit circuit fits within its coupling map
import qiskit
from qiskit.test.mock import FakeAthens

# FIX: backend instantiated with the 1-qubit FakeArmonk -> use FakeAthens, because it has enough qubits for the circuit
backend = FakeAthens()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
