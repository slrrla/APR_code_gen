from qiskit import QuantumCircuit

sub = QuantumCircuit(2, name='my_gate')
sub.h(0)
sub.cx(0, 1)
custom_gate = sub.to_gate()

qc = QuantumCircuit(2)
qc.append(custom_gate, [0, 1])

qc_decomposed = qc.decompose()
qasm_str = qc_decomposed.qasm()
print(qasm_str)
