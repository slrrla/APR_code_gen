from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

qc.measure(q, c)

# FIX: gates were conditioned on single bits separately, not jointly -> condition both X gates on the register value 3 (c[0]=1 and c[1]=1, c[2]=0), because c_if on a register can express the AND of several bits for multiple operations
qc.x(q[0]).c_if(c, 3)
qc.x(q[1]).c_if(c, 3)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
