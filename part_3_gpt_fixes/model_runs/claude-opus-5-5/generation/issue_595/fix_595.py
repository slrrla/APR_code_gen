from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
# FIX: no unitary was saved in the circuit -> added circ.save_unitary(), because Aer only returns a unitary in the result when a save_unitary instruction is present
circ.save_unitary()

# FIX: default AerSimulator() uses an automatic (statevector-like) method -> set method='unitary', because the unitary can only be computed and saved by the unitary simulation method
simulator = AerSimulator(method='unitary')
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
