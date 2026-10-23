import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

# FIX: theta was computed as complex from acos of a complex value -> use the real magnitude of the |0> amplitude, because cos(theta/2) = |(1+i)/sqrt(3)| = sqrt(2/3) is real
theta = 2*math.acos(abs((1+1.j)/math.sqrt(3)))
print('theta : ', theta)

sinValue = cmath.sin(theta/2)
print(sinValue)

phase = -1*(1.j/cmath.sqrt(3))/sinValue
# FIX: phi was the log of a unit complex number, which is the absolute phase of |1> only -> use the relative phase arg(|1> amplitude) - arg(|0> amplitude), because u3 applies the phase relative to |0>
phi = cmath.phase(-1.j/cmath.sqrt(3)) - cmath.phase((1+1.j)/cmath.sqrt(3))
print('phi : ', phi)

circ = QuantumCircuit(1, 1)
circ.u3(theta, phi, 0, 0)

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
