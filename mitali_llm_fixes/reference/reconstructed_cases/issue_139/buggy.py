from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, BasicAer

register = 5

q = QuantumRegister(9)
c = ClassicalRegister(9)
qc = QuantumCircuit(q, c)

qc.h(q[register])

simulator = BasicAer.get_backend('qasm_simulator')

qc.measure(q[register], c[register])
job = execute(qc, simulator, shots=1000)
result = job.result()
counts = result.get_counts(qc)
print("\nTotal count for 0 and 1 are:", counts)
