from qiskit import QuantumCircuit
from qiskit.circuit.library import UCRYGate
from qiskit.providers.basic_provider import BasicProvider

# Build a simple circuit that uses a "ucry" (uniformly controlled RY) gate
qc_combine = QuantumCircuit(2)
angles = [0.5, 1.0]
qc_combine.append(UCRYGate(angles), [1, 0])
qc_combine.measure_all()

shots_used = 1024

backend = BasicProvider().get_backend("basic_simulator")
print(qc_combine.draw())
job = backend.run(qc_combine, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_combine)
print(counts)
