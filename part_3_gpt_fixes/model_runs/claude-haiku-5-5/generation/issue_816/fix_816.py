from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

circ = QuantumCircuit(2, 2)
circ.h(0)
circ.cx(0, 1)
circ.measure([0, 1], [0, 1])

simulator = AerSimulator()

# FIX: get_memory() had no per-shot data because run() did not record memory -> added memory=True to the run call, because memory=True makes Aer store each shot's classical bit outcome so get_memory() can return them
result = simulator.run(circ, shots=10, memory=True).result()
memory = result.get_memory(circ)
print(memory)
