from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: each X was conditioned independently on its own bit -> nested if_test on c[0]==1 and c[1]==1 wrapping both X gates, because the recovery must apply both gates only when both bits are 1
with qc.if_test((c[0], 1)):
    with qc.if_test((c[1], 1)):
        qc.x(q[0])
        qc.x(q[1])

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
