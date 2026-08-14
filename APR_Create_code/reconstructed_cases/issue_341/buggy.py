from qiskit.providers.fake_provider import FakeHanoiV2
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit

# Use a fake backend as-is, without increasing its noise
backend = FakeHanoiV2()

sim = AerSimulator.from_backend(backend)

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

result = sim.run(qc).result()
print(result.get_counts())
