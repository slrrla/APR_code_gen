import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

# We create the quantum state manually first
arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

# U3 angles are real; separate each amplitude's magnitude and phase.
theta = 2*math.acos(abs((1+1.j)/math.sqrt(3)))
print('theta : ', theta)

sinValue = math.sin(theta/2)
print(sinValue)

alpha_phase = cmath.phase((1+1.j)/math.sqrt(3))
beta_phase = cmath.phase(-1.j/math.sqrt(3))
phi = beta_phase - alpha_phase
print('phi : ', phi)

# Use these theta and phi to create the circuit
circ = QuantumCircuit(1, 1)
# The U3 gate supplies the relative phase; retain the overall phase too.
circ.global_phase = alpha_phase
circ.u3(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
