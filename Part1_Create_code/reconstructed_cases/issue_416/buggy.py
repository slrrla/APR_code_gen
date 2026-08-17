from qiskit import *

circuit = QuantumCircuit(3)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.cx(2, 0)
circuit.draw('mpl')

# No coupling map restriction is applied, so transpiling
# does not adapt the circuit to any limited connectivity.
transpiled = transpile(circuit)
transpiled.draw('mpl')
