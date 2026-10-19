from qiskit_aer import AerSimulator

params = {'ncores': 4}

# A small circuit - too small to trigger multi-threaded parallelization
from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure(range(3), range(3))

backend = AerSimulator()
backend.set_options(max_parallel_threads=params['ncores'])

result = backend.run(qc).result()
counts = result.get_counts()
print(counts)
