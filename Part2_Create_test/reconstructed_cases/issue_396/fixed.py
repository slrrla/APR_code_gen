from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator

targets = ("101", "110")
oracle = QuantumCircuit(3)

for target in targets:
    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            oracle.x(qubit)

    # H-MCX-H applies a phase flip to the selected target state.
    oracle.h(2)
    oracle.mcx([0, 1], 2)
    oracle.h(2)

    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            oracle.x(qubit)

grover_op = GroverOperator(oracle)
print(grover_op)
