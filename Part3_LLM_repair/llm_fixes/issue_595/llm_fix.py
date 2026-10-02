from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
# FIX: no unitary was saved -> add a save_unitary instruction, because AerSimulator only returns saved results
circ.save_unitary()

simulator = AerSimulator()
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)

