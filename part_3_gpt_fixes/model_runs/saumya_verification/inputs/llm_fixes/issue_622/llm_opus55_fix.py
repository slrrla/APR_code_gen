import qiskit
# FIX: imported 1-qubit FakeArmonk -> import 5-qubit FakeVigo, because the 2-qubit circuit cannot fit on a 1-qubit device
from qiskit.test.mock import FakeVigo

# FIX: backend = FakeArmonk() -> backend = FakeVigo(), because the coupling map must have at least 2 qubits for the CX circuit
backend = FakeVigo()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)

