from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# FIX: Default simulation did not compute or save a unitary -> use the unitary method and save it, because get_unitary requires saved unitary data.
simulator = AerSimulator(method="unitary")
circ.save_unitary()
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)

