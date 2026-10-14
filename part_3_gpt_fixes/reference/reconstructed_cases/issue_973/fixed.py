from qiskit import QuantumCircuit

N = 10000
qc = QuantumCircuit(1)
qc.x(0)
qc.barrier()
qc = qc.repeat(N)
qc.decompose(reps=2).draw()
