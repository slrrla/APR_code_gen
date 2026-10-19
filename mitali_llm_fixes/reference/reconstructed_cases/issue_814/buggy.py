from qiskit import QuantumCircuit, execute, Aer

qc = QuantumCircuit(3, 3)
qc.h(0)
qc.h(1)
qc.h(2)
qc.measure([0, 1, 2], [0, 1, 2])

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=41)
result = job.result()
res = result.get_counts(qc)

# This raises a KeyError if '011' never occurred
zero_count = res['011']
print(zero_count)
