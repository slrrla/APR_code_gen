import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

# FIX: theta was computed from acos of a complex amplitude, giving a complex angle -> use acos of the amplitude's magnitude, because cos(theta/2) must equal |alpha| and u3 needs a real angle
theta = 2*math.acos(abs((1+1.j)/math.sqrt(3)))
print('theta : ', theta)

sinValue = cmath.sin(theta/2)
print(sinValue)

phase = -1*(1.j/cmath.sqrt(3))/sinValue
# FIX: phi was a complex log that ignored the phase of the |0> amplitude -> use the phase of the |1> amplitude minus the phase of the |0> amplitude, because the relative phase is a real number and the global phase is unobservable
phi = cmath.phase(phase) - cmath.phase(1+1.j)
print('phi : ', phi)

circ = QuantumCircuit(1, 1)
circ.u3(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
