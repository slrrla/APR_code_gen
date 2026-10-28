from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(3 + 1)
qc.h(0)
qc.h(1)
qc.h(2)
qc.mct([0, 1, 2], 3, mode="noancilla")

qc.save_statevector()

qc = qc.reverse_bits()
qc.measure_all()

backend = AerSimulator()
job = backend.run(qc, shots=1000)
counts = job.result().get_counts()
print(counts)
