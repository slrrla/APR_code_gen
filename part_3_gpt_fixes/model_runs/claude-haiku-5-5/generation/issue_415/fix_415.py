import math
import cmath
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

arb_quantum_state = ((1+1.j)/math.sqrt(3))*ket_0 - (1.j/math.sqrt(3))*ket_1
print(arb_quantum_state)

# FIX: theta was computed as 2*cmath.acos of a complex value (complex result) -> take acos of the real modulus of the |0> amplitude, because cos(theta/2) = |(1+i)/sqrt(3)| is real and this gives a real angle
theta = 2*math.acos(abs((1+1.j)/math.sqrt(3)))
print('theta : ', theta)

sinValue = cmath.sin(theta/2)
print(sinValue)

phase = -1*(1.j/cmath.sqrt(3))/sinValue
# FIX: phi was a complex log (complex result that u3 rejects) -> use the real difference of the two amplitude phases, because the relative phase between |1> and |0> is arg(b) - arg(a)
phi = cmath.phase(-1.j/math.sqrt(3)) - cmath.phase((1+1.j)/math.sqrt(3))
print('phi : ', phi)

circ = QuantumCircuit(1, 1)
circ.u3(theta, phi, 0, 0)
# FIX: u3 produces the state up to a global phase -> set circ.global_phase to arg of the |0> amplitude, because this recovers the exact target vector including its overall phase
circ.global_phase = cmath.phase((1+1.j)/math.sqrt(3))

results = execute(circ, backend=Aer.get_backend('statevector_simulator')).result()
quantum_state = results.get_statevector(circ, decimals=3)
print(quantum_state)
