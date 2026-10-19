from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

# Construct quantum circuit without measure
circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# Old style: try to get unitary using outdated API (missing save_unitary call)
simulator = AerSimulator()
circ = transpile(circ, simulator)

# Run and get unitary
result = simulator.run(circ).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
