from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.random import random_circuit

params = {'ncores': 4}

num_circuits = 200
num_qubits = 20
depth = 30
circuits = []
for n in range(num_circuits):
    circuits.append(random_circuit(num_qubits, depth, max_operands=2, measure=True))

backend = AerSimulator(method='statevector')
tr_circuits = transpile(circuits, backend=backend)

backend.set_options(
    max_parallel_threads=0,
    max_parallel_experiments=0,
    max_parallel_shots=1,
    statevector_parallel_threshold=16
)

result = backend.run(tr_circuits).result()
counts = result.get_counts()
print(counts)
