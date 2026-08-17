from qiskit import QuantumCircuit

qc1 = QuantumCircuit(1, name='qc1')
qc1.x(0)

qc2 = QuantumCircuit(1, name='qc2')
qc2.h(0)
qc2.append(qc1, [0])
qc2.z(0)

c_qc2 = qc2.to_gate().control(1)
