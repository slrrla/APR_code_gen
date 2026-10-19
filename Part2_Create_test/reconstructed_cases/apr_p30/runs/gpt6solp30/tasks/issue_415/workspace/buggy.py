import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

# We create the quantum state manually first
arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

theta = 2*math.acos(abs(arb_quantum_state[0]))
print('theta : ', theta)

sinValue = math.sin(theta/2)
print(sinValue)

global_phase = cmath.phase(arb_quantum_state[0])
phase = arb_quantum_state[1] / (sinValue * cmath.exp(1.j * global_phase))
phi = cmath.phase(phase)
print('phi : ', phi)

# Use these theta and phi to create the circuit
circ = QuantumCircuit(1, 1)
# A U gate uses real angles; restore the phase of the |0> amplitude.
circ.global_phase = global_phase
circ.u(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
