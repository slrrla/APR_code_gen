import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

# We create the quantum state manually first
arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

# Factor out the phase of the |0> amplitude to obtain real gate angles.
global_phase = cmath.phase(arb_quantum_state[0])
theta = 2*math.acos(abs(arb_quantum_state[0]))
print('theta : ', theta)

sinValue = math.sin(theta/2)
print(sinValue)

phase = arb_quantum_state[1] * cmath.exp(-1.j*global_phase) / sinValue
phi = cmath.phase(phase) % (2*math.pi)
print('phi : ', phi)

# Use these theta and phi to create the circuit
circ = QuantumCircuit(1, 1)
circ.global_phase = global_phase
circ.u(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
