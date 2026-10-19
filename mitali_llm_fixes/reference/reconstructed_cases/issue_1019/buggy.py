import qiskit
from qiskit import QuantumCircuit, execute, Aer

# construct my circuits and append to qcircuits
qcircuits = []
for i in range(3):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    qcircuits.append(qc)

backend = Aer.get_backend('qasm_simulator')
n_shots = 1024
optimization_level = 1

job = qiskit.execute(
    qcircuits,
    backend,
    optimization_level=optimization_level,
    shots=n_shots
)

counts = job.result().get_counts()
# counts is returned in the order the parallel jobs finished,
# not necessarily the order qcircuits was constructed in
print(counts)
