from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: c_if compares a whole classical register, not an individual bit -> enumerate register values for each bit, because each bit can be 1 under multiple register values
qc.x(q[0]).c_if(c, 1)
qc.x(q[0]).c_if(c, 3)
qc.x(q[0]).c_if(c, 5)
qc.x(q[0]).c_if(c, 7)
qc.x(q[1]).c_if(c, 2)
qc.x(q[1]).c_if(c, 3)
qc.x(q[1]).c_if(c, 6)
qc.x(q[1]).c_if(c, 7)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))

