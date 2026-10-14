from qiskit import *

circuit = QuantumCircuit(2, 2)
circuit.cx(0, 1)

simulator = Aer.get_backend("unitary_simulator")
result = execute(circuit, backend=simulator).result()
unitary = result.get_unitary()

print(circuit.draw())
print(unitary)
