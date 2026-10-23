from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: Each X used an independent condition -> nest both X gates under both bit checks, because both operations must require c[0] == 1 and c[1] == 1.
with qc.if_test((c[0], 1)):
    with qc.if_test((c[1], 1)):
        qc.x(q[0])
        qc.x(q[1])

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))

