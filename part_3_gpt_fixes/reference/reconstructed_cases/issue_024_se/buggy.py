from qiskit import QuantumCircuit

# Build a custom gate from a sub-circuit
sub = QuantumCircuit(2, name='my_gate')
sub.h(0)
sub.cx(0, 1)
custom_gate = sub.to_gate()

# Main circuit using the custom gate
qc = QuantumCircuit(2)
qc.append(custom_gate, [0, 1])

# User only knows about from_qasm_file / qasm export, not how to ungroup
qasm_str = qc.qasm()
print(qasm_str)
