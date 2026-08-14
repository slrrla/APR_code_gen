from qiskit import QuantumCircuit
from qiskit_textbook.problems import dj_problem_oracle

# Author assumed the oracle acts on a fixed number of qubits (n=4)
# instead of checking how many qubits the oracle gate actually needs.
oracle = dj_problem_oracle(1)

n = 4  # hardcoded guess, not derived from the oracle itself

dj_circuit = QuantumCircuit(n + 1, n)

for qubit in range(n):
    dj_circuit.h(qubit)
dj_circuit.x(n)
dj_circuit.h(n)

# BUG: oracle actually needs n+1 qubits, but only n are given here
dj_circuit.append(oracle, range(n))

for qubit in range(n):
    dj_circuit.h(qubit)

dj_circuit.barrier()
for i in range(n):
    dj_circuit.measure(i, i)

print(dj_circuit)
