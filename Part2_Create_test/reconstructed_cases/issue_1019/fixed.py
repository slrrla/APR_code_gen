import qiskit
from qiskit import QuantumCircuit, execute, Aer

# construct my circuits and append to qcircuits
qcircuits = []
for i in range(3):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    qcircuits.append(qc)

# number input circuits in ascending order
for i in range(len(qcircuits)):
    qcircuits[i].name = "circuit_" + str(i)

backend = Aer.get_backend('qasm_simulator')
n_shots = 1024
optimization_level = 1

job = qiskit.execute(
    qcircuits,
    backend,
    optimization_level=optimization_level,
    shots=n_shots
)

result_dict = job.result().to_dict()["results"]
result_counts = job.result().get_counts()

# initialize list to store ordered results
results_ordered = [None] * len(qcircuits)
for i in range(len(qcircuits)):
    name = result_dict[i]["header"]["name"]
    n = int(name.split('_')[1])  # index of circuit in input list
    results_ordered[n] = result_counts[i]  # add to result list at same index

print(results_ordered)
