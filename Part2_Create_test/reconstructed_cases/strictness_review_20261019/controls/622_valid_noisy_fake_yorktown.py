import qiskit
from qiskit.providers.fake_provider import FakeYorktown
backend = FakeYorktown()
qc = qiskit.QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
job_exp = qiskit.execute(qc, backend=backend, shots=1024, seed_simulator=622)
