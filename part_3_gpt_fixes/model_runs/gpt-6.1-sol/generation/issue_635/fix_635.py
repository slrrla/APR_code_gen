from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: Each X used an independent condition -> condition both X gates on register values 3 or 7, because these require c[0] == c[1] == 1 regardless of c[2]
qc.x(q[0]).c_if(c, 3)
qc.x(q[1]).c_if(c, 3)
qc.x(q[0]).c_if(c, 7)
qc.x(q[1]).c_if(c, 7)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
