from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

q = QuantumRegister(3)

# Only the first two classical bits are used for the condition.
syndrome = ClassicalRegister(2, "syndrome")
result = ClassicalRegister(3, "result")

qc = QuantumCircuit(q, syndrome, result)

# Measure the two syndrome bits.
qc.measure(q[0], syndrome[0])
qc.measure(q[1], syndrome[1])

# syndrome == 3 means syndrome[0] == 1 and syndrome[1] == 1.
qc.x(q[0]).c_if(syndrome, 3)
qc.x(q[1]).c_if(syndrome, 3)

# Measure the final quantum state separately.
qc.measure(q, result)

backend = Aer.get_backend("qasm_simulator")
job = execute(qc, backend, shots=1024)
result_data = job.result()

print(result_data.get_counts(qc))
