from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
import numpy as np

theta = np.pi / 3  # unknown angle we want to estimate

q = QuantumRegister(1, 'q')
c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(q, c)

# prepare |phi> = 1/sqrt(2)(|0> + e^{i theta}|1>)
circuit.h(q[0])
circuit.u1(theta, q[0])

# naive measurement directly in the computational (Z) basis
# this gives 50/50 outcomes regardless of theta, revealing nothing about it
circuit.measure(q[0], c[0])

backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()
counts = result.get_counts(circuit)
print(counts)
