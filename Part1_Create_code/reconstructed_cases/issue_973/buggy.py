from qiskit import QuantumCircuit

N = 10000
qc = QuantumCircuit(1)
for i in range(N):
    qc.x(0)
    qc.barrier()
