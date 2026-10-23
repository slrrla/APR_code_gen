from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
# FIX: no save instruction was added to the circuit -> added circ.save_unitary(), because Aer only returns the unitary when it is saved explicitly
circ.save_unitary()

# FIX: default AerSimulator method cannot compute a unitary -> set method='unitary', because the unitary simulation method is required for save_unitary
simulator = AerSimulator(method='unitary')
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
