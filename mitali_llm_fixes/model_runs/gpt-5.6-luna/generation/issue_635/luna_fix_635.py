from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: a single classical bit is not a valid c_if condition -> use the full register's encoded value, because c_if accepts a ClassicalRegister
qc.x(q[0]).c_if(c, 1)
# FIX: a single classical bit is not a valid c_if condition -> use the full register's encoded value, because c_if accepts a ClassicalRegister
qc.x(q[1]).c_if(c, 2)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
