import qiskit

qc = qiskit.QuantumCircuit(2, 2)
qc.h(0)
qc.cf(0, 1)
