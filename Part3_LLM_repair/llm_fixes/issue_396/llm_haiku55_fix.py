from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator

targets = ['101', '110']

# FIX: Statevector.from_label cannot take a list and does not give a phase oracle circuit -> built a 3-qubit QuantumCircuit that flips the phase of each target state, because GroverOperator needs a circuit oracle that marks every solution with a -1 phase
oracle = QuantumCircuit(3)
for target in targets:
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            oracle.x(i)
    oracle.h(2)
    oracle.mcx([0, 1], 2)
    oracle.h(2)
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            oracle.x(i)

grover_op = GroverOperator(oracle)
print(grover_op)
