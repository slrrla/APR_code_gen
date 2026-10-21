from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

circ = QuantumCircuit(2, 2)
circ.h(0)
circ.cx(0, 1)
circ.measure([0, 1], [0, 1])

simulator = AerSimulator()

# FIX: run was called without memory=True -> added memory=True, because get_memory requires per-shot results to be stored by the simulator
result = simulator.run(circ, shots=10, memory=True).result()
memory = result.get_memory(circ)
print(memory)
