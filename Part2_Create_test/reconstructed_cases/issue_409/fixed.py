import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile, execute
from qiskit import Aer
from numpy import pi

# Reference numpy computation for comparison
M = np.array([[0, 0.2, 0.8], [0.5, 0, 0.5], [0.1, 0.9, 0]])
v0 = np.array([1, 0, 0])
v1 = v0.dot(M)
print(v1)
v2 = v0.dot(np.linalg.matrix_power(M, 2))
print(v2)
v3 = v0.dot(np.linalg.matrix_power(M, 3))
print(v3)

# Inilialise registers
qreg_q = QuantumRegister(6, 'q')
creg_c = ClassicalRegister(3, 'c')

# Create Markov Step as a circuit
markov_step = QuantumCircuit(qreg_q)

# From state 0 to state 1 and 2
# cu3 is replaced with mcu3 (multi-controlled U3) since some backends
# do not support the plain cu3 gate; the control qubit is passed as a list.
markov_step.mcu3(2 * np.arccos(np.sqrt(M[0, 1])), pi / 2, pi / 2, [qreg_q[0]], qreg_q[4])
markov_step.ccx(qreg_q[4], qreg_q[0], qreg_q[5])
markov_step.cx(qreg_q[0], qreg_q[4])

# From state 1 to state 0 and 2
markov_step.mcu3(2 * np.arccos(np.sqrt(M[1, 2])), pi / 2, pi / 2, [qreg_q[1]], qreg_q[5])
markov_step.ccx(qreg_q[5], qreg_q[1], qreg_q[3])
markov_step.cx(qreg_q[1], qreg_q[5])

# From state 2 to state 0 and 1
markov_step.mcu3(2 * np.arccos(np.sqrt(M[2, 0])), pi / 2, pi / 2, [qreg_q[2]], qreg_q[3])
markov_step.ccx(qreg_q[3], qreg_q[2], qreg_q[4])
markov_step.cx(qreg_q[2], qreg_q[3])

# Swap
markov_step.swap(qreg_q[0], qreg_q[3])
markov_step.swap(qreg_q[1], qreg_q[4])
markov_step.swap(qreg_q[2], qreg_q[5])

# Initialise circuit
circuit = QuantumCircuit(qreg_q, creg_c)

# Initialise state (1,0,0)
circuit.x(0)

# Do the markov step n times
n = 3
for _ in range(n):
    for ins in markov_step:
        circuit.append(ins[0], ins[1], ins[2])
    circuit.reset(qreg_q[3:])

# Measure outcome
circuit.measure(qreg_q[:3], creg_c)

backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend)
result = job.result()
counts = result.get_counts(circuit)
print(counts)
