from qiskit import QuantumCircuit

# Build a small subcircuit FC that explicitly contains an identity gate
FC = QuantumCircuit(3)
FC.id(0)
FC.h(1)
FC.cx(1, 2)

# Instead of converting FC into a gate, compose it directly into the circuit
circuit = QuantumCircuit(3)
circuit = circuit.compose(FC, [0, 1, 2])
circuit = circuit.compose(FC, [0, 1, 2])

# Now iterate over the decomposed circuit to see all constituent elements
for instruction, qarg, carg in circuit.decompose():
    print(instruction)
