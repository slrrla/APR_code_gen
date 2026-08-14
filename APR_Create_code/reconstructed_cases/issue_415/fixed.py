import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

# We create the quantum state manually first
arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

# theta and phi must be real: account for the global phase gamma so that
# cos(theta/2) and sin(theta/2) are real numbers.
# |psi> = e^{i*pi/4} ( sqrt(2/3)|0> + (1/sqrt(3))e^{i*5*pi/4}|1> )
theta = 2*math.acos(math.sqrt(2/3))
phi = 5*math.pi/4
print('theta : ', theta)
print('phi : ', phi)

# Use these real theta and phi to create the circuit
circ = QuantumCircuit(1, 1)
circ.u3(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
