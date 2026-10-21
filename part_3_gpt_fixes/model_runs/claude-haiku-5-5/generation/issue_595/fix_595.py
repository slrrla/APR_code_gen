from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# FIX: default AerSimulator method is statevector, which does not produce a unitary -> set method='unitary', because the unitary method is required for result.get_unitary to return the circuit's matrix
simulator = AerSimulator(method='unitary')
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
