from qiskit import QuantumCircuit

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

for instruction in circ.data:
    print(instruction.operation.name, instruction.qubits)
