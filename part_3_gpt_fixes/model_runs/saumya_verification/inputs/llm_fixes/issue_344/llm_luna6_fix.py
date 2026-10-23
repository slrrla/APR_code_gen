import numpy as np
from qiskit import QuantumCircuit, BasicAer, execute
from qiskit import quantum_info

circuit6 = QuantumCircuit(2)
circuit6.h(0)
circuit6.cx(0, 1)
circuit6.ry(1.0, 1)

simulator = BasicAer.get_backend('statevector_simulator')
result6 = execute(circuit6, simulator).result()
# FIX: rounding the amplitudes makes the statevector fail normalization validation -> keep full precision, because entropy requires a valid normalized state
outputstate6 = result6.get_statevector(circuit6)
probability = np.abs(np.array(outputstate6))**2
outstatevector = quantum_info.states.Statevector(outputstate6)
print(type(outstatevector))
print(type(outputstate6))
print(outputstate6)
print(quantum_info.entropy(outputstate6))

