from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
# FIX: no instruction saved the unitary -> added circ.save_unitary(), because Aer only returns data that is explicitly saved
circ.save_unitary()

# FIX: default simulation method cannot compute unitaries -> use method='unitary', because the unitary method builds the full circuit matrix
simulator = AerSimulator(method='unitary')
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)

