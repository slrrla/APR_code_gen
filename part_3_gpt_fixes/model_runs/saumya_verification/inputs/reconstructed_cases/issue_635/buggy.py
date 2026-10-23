from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# Attempt to implement: if c[0]==1 and c[1]==1: qc.x(q[0]); qc.x(q[1])
# by conditioning on individual classical bits directly.
qc.x(q[0]).c_if(c[0], 1)
qc.x(q[1]).c_if(c[1], 1)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
