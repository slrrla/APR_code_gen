from qiskit import *

circuit = QuantumCircuit(3)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.cx(2, 0)
circuit.draw('mpl')

# Restrict transpilation to a directed linear connectivity map
# 0 -> 1 -> 2, forcing the circuit to be adapted accordingly.
transpiled = transpile(circuit, coupling_map=[[0, 1], [1, 2]])
transpiled.draw('mpl')

# Additionally fix the initial logical-to-physical qubit layout.
transpiled = transpile(circuit, coupling_map=[[0, 1], [1, 2]], initial_layout=[0, 1, 2])
transpiled.draw('mpl')
