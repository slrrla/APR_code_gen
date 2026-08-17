from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.result import marginal_counts

qc = QuantumCircuit(4)
qc.h([0, 1, 2, 3])
qc.cx(1, 3)
qc.cx(2, 0)
qc.measure_all()

sim = AerSimulator()
job = sim.run(qc, shots=1024)
res = job.result().get_counts()
print(res)

new_counts = marginal_counts(res, [0, 1])  # To get the counts from qubit 0 and 1
print(new_counts)
