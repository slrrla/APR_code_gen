from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# FIX: The default simulation method does not compute a unitary -> select the unitary method, because the requested result is a unitary matrix
simulator = AerSimulator(method="unitary")
# FIX: The circuit does not save its unitary -> add save_unitary(), because get_unitary() requires a saved unitary in the result
circ.save_unitary()
circ = transpile(circ, simulator)

result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
