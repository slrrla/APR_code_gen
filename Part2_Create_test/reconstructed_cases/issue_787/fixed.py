from qiskit import QuantumCircuit
from qiskit_textbook.problems import dj_problem_oracle

oracle = dj_problem_oracle(1)

# FIX: determine the number of "input" qubits from the oracle itself.
# The oracle gate has n+1 qubits (n input qubits + 1 output qubit).
n = oracle.num_qubits - 1

dj_circuit = QuantumCircuit(n + 1, n)

for qubit in range(n):
    dj_circuit.h(qubit)
dj_circuit.x(n)
dj_circuit.h(n)

# Now the oracle is appended to all n+1 qubits it actually expects.
dj_circuit.append(oracle, range(n + 1))

for qubit in range(n):
    dj_circuit.h(qubit)

dj_circuit.barrier()
for i in range(n):
    dj_circuit.measure(i, i)

print(dj_circuit)
