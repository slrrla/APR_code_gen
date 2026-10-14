from qiskit import QuantumCircuit

# Build a custom gate from a sub-circuit
sub = QuantumCircuit(2, name='my_gate')
sub.h(0)
sub.cx(0, 1)
custom_gate = sub.to_gate()

# Main circuit using the custom gate
qc = QuantumCircuit(2)
qc.append(custom_gate, [0, 1])

# Decompose the custom gate to ungroup it into its component gates
qc_decomposed = qc.decompose()

qasm_str = qc_decomposed.qasm()
print(qasm_str)
