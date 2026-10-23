import numpy as np
from qiskit import QuantumCircuit, BasicAer, execute
from qiskit import quantum_info

# minimal circuit producing a non-trivial statevector
circuit6 = QuantumCircuit(2)
circuit6.h(0)
circuit6.cx(0, 1)
circuit6.ry(1.0, 1)

simulator = BasicAer.get_backend('statevector_simulator')  # the device to run on
result6 = execute(circuit6, simulator).result()
# do not truncate decimals, otherwise the statevector is no longer normalized
outputstate6 = result6.get_statevector(circuit6)
probability = np.abs(np.array(outputstate6))**2
outstatevector = quantum_info.states.Statevector(outputstate6)
print(type(outstatevector))
print(type(outputstate6))
print(outputstate6)
# pass the valid Statevector object (norm 1) to entropy
print(quantum_info.entropy(outstatevector))
