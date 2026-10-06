import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

# We create the quantum state manually first
arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

theta = 2*cmath.acos((1+1.j)/cmath.sqrt(3))
print('theta : ', theta)

sinValue = cmath.sin(theta/2)
print(sinValue)

phase = -1*(1.j/cmath.sqrt(3))/sinValue
phi = cmath.log(phase)/1.j
print('phi : ', phi)

# Use these theta and phi to create the circuit
circ = QuantumCircuit(1, 1)
# Verify why complex values are not allowed
# circ.u3(theta.real, phi.real, 0, 0)
circ.u3(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
