from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
# FIX: execute/Aer no longer importable from qiskit -> import Aer from qiskit_aer, because they were removed from qiskit in 1.0
from qiskit_aer import Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: separate per-gate c_if conditions (c_if also removed) -> nested if_test blocks applying both X gates, because the recovery must run only when c[0]==1 and c[1]==1 jointly
with qc.if_test((c[0], 1)):
    with qc.if_test((c[1], 1)):
        qc.x(q[0])
        qc.x(q[1])

backend = Aer.get_backend('qasm_simulator')
# FIX: execute(...) removed -> backend.run on transpiled circuit, because execute no longer exists in Qiskit
job = backend.run(transpile(qc, backend), shots=1024)
result = job.result()
print(result.get_counts(qc))
