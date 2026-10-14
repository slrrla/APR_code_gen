from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

circ = QuantumCircuit(2, 2)
circ.h(0)
circ.cx(0, 1)
circ.measure([0, 1], [0, 1])

simulator = AerSimulator()

# Run without memory=True, so per-shot results are not recorded
result = simulator.run(circ, shots=10).result()
memory = result.get_memory(circ)  # raises: no memory data collected
print(memory)
