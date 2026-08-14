from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.providers.fake_provider import FakeCairo

# Simple circuit to run
qc_combine = QuantumCircuit(2)
qc_combine.h(0)
qc_combine.cx(0, 1)
qc_combine.measure_all()

shots_done = 1024

# provider = IBMQ.load_account()
# using a local fake backend instead of a real hardware provider call
backend_cairo = FakeCairo()

# Directly build a simulator that mimics the real device
# (noise model, coupling map, and basis gates) with a single call
backend = AerSimulator.from_backend(backend_cairo)

transpiled_circuit = transpile(qc_combine, backend)
result = backend.run(transpiled_circuit, shots=shots_done).result()
print(result.get_counts())
