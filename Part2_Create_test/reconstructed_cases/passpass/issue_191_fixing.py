from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
import numpy as np

theta = np.pi / 3

q = QuantumRegister(1, 'q')
c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(q, c)

circuit.h(q[0])
circuit.p(theta, q[0])
circuit.h(q[0])
circuit.measure(q[0], c[0])

backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()
counts = result.get_counts(circuit)
print(counts)
print("Estimated cos(theta):", (counts.get('0', 0) - counts.get('1', 0)) / 1024)
