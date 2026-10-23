from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

circ = QuantumCircuit(2, 2)
circ.h(0)
circ.cx(0, 1)
circ.measure([0, 1], [0, 1])

simulator = AerSimulator()

# FIX: run() was missing memory=True, so per-shot results were not stored and get_memory() failed -> added memory=True to the run call, because this makes Aer keep each shot's classical bitstring for get_memory().
result = simulator.run(circ, shots=10, memory=True).result()
memory = result.get_memory(circ)
print(memory)
