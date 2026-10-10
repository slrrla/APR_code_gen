from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# FIX: The default simulation method does not ensure unitary simulation -> select "unitary", because the full circuit operator is needed.
simulator = AerSimulator(method="unitary")
# FIX: No unitary was saved in the result -> add save_unitary(), because get_unitary() requires saved unitary data.
circ.save_unitary()
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)

