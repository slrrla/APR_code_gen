from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
# FIX: no unitary was saved in the circuit -> added circ.save_unitary(), because AerSimulator only returns the unitary if a save_unitary instruction is present
circ.save_unitary()

# FIX: default simulator method cannot produce a unitary -> set method='unitary', because the unitary simulation method is needed for save_unitary
simulator = AerSimulator(method='unitary')
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
