from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: q[0] depended only on c[0] -> condition on register values 3 or 7, because both require c[0] and c[1] to be 1 regardless of c[2]
qc.x(q[0]).c_if(c, 3)
qc.x(q[0]).c_if(c, 7)
# FIX: q[1] depended only on c[1] -> condition on register values 3 or 7, because both operations must use the same joint condition
qc.x(q[1]).c_if(c, 3)
qc.x(q[1]).c_if(c, 7)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))

