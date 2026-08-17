from qiskit import QuantumCircuit

qc1 = QuantumCircuit(1, name='qc1')
qc1.x(0)
print(qc1)

qc2 = QuantumCircuit(1, name='qc2')
qc2.h(0)
qc2.append(qc1.to_gate(), [0])
qc2.z(0)
print(qc2)

xs_gate = qc2.to_gate()
cxs_gate = xs_gate.control()

circuit = QuantumCircuit(2)
circuit.append(cxs_gate, [0, 1])
print('\n New circuit with controlled:\n', circuit)
print('\n Decomposed new circuit:\n', circuit.decompose())
