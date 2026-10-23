import qiskit
# FIX: FakeArmonk has only 1 qubit but the circuit needs 2 -> imported FakeVigo (5-qubit mock backend), because it can host the 2-qubit circuit
from qiskit.test.mock import FakeVigo

# FIX: backend was FakeArmonk (1 qubit) -> changed to FakeVigo, because the transpiler requires the circuit's qubit count to fit the coupling map
backend = FakeVigo()

q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
