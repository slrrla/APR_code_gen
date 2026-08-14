from qiskit import QuantumCircuit

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# Only decomposition available - always uses IBMQ-native basis gates,
# no way to specify a custom (e.g. ion-trap) basis gate set
decomposed = circ.decompose()

print(decomposed)
