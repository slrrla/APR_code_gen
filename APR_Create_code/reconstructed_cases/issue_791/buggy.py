from qiskit import QuantumCircuit

# Build a small subcircuit FC that explicitly contains an identity gate
FC = QuantumCircuit(3)
FC.id(0)
FC.h(1)
FC.cx(1, 2)

# Convert the subcircuit into a single gate/instruction
gate = FC.to_instruction()

# Build a bigger circuit that uses this gate
circuit = QuantumCircuit(3)
circuit.append(gate, [0, 1, 2])
circuit.append(gate, [0, 1, 2])

# Iterate over the elements of the circuit - only shows the composite gate,
# not its constituent elements (identity gate etc.)
for instruction, qarg, carg in circuit:
    print(instruction)
