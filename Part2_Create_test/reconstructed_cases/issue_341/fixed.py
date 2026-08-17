from qiskit.providers.fake_provider import FakeHanoiV2
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit

backend = FakeHanoiV2()

# Increase the noise of the backend by modifying the target in place.
# Here we raise the measurement error on qubit 0 to 50%.
backend.target['measure'][(0,)].error = 0.5

sim = AerSimulator.from_backend(backend)

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

result = sim.run(qc).result()
print(result.get_counts())
