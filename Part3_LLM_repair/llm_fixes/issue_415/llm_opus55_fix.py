import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

# FIX: acos of a complex amplitude gave a complex theta -> use math.acos of the amplitude's magnitude, because u3 needs a real angle and cos(theta/2) must equal |alpha|
theta = 2*math.acos(abs((1+1.j)/cmath.sqrt(3)))
print('theta : ', theta)

sinValue = cmath.sin(theta/2)
print(sinValue)

# FIX: ignored the phase of the |0> amplitude -> divide out that phase, because only the relative phase (global phase removed) can be encoded by u3
phase = -1*(1.j/cmath.sqrt(3))/sinValue / cmath.exp(1.j*cmath.phase((1+1.j)/cmath.sqrt(3)))
# FIX: complex log produced a complex phi -> use cmath.phase, because it returns the real relative phase angle u3 accepts
phi = cmath.phase(phase)
print('phi : ', phi)

circ = QuantumCircuit(1, 1)
circ.u3(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
