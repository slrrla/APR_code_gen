from qiskit import QuantumCircuit

# Build a sub-circuit and append it onto specific qubits of the main circuit
# instead of trying to construct a register from existing qubits.
sub_circuit = QuantumCircuit(2)
sub_circuit.h(range(2))

circuit = QuantumCircuit(4)
qr = circuit.qregs[0]
circuit.x(range(4))

circuit = circuit.append(sub_circuit.to_instruction(), [qr[0], qr[1]])
