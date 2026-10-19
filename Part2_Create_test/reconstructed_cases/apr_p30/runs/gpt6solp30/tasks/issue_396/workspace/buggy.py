from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator


# Desired marked (solution) states for the oracle
targets = ['101', '110']

# Flip the phase of each marked basis state. Bitstrings are ordered q2 q1 q0.
oracle = QuantumCircuit(len(targets[0]))
for target in targets:
    zero_qubits = [i for i, bit in enumerate(reversed(target)) if bit == '0']
    for qubit in zero_qubits:
        oracle.x(qubit)
    oracle.h(2)
    oracle.mcx([0, 1], 2)
    oracle.h(2)
    for qubit in zero_qubits:
        oracle.x(qubit)

grover_op = GroverOperator(oracle)
print(grover_op)
