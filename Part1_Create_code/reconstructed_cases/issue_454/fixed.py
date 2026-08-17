from qiskit import QuantumCircuit
from qiskit.circuit.library import UCRYGate
from qiskit.providers.basic_provider import BasicProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Build a simple circuit that uses a "ucry" (uniformly controlled RY) gate
qc_combine = QuantumCircuit(2)
angles = [0.5, 1.0]
qc_combine.append(UCRYGate(angles), [1, 0])
qc_combine.measure_all()

shots_used = 1024

backend = BasicProvider().get_backend("basic_simulator")

# Transpile the circuit into a basis the simulator understands
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
qc_combine = pm.run(qc_combine)

print(qc_combine.draw())
job = backend.run(qc_combine, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_combine)
print(counts)
