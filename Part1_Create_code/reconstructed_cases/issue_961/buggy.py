from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeProvider

# create a bell circuit
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])

# try to get a fake backend for ibm_brisbane -- this backend name does not
# exist in FakeProvider, so this raises an error (backend not present)
provider = FakeProvider()
backend = provider.get_backend('fake_brisbane')

# transpile to backend
circ = transpile(circuit, backend=backend)

# run on the fake backend
job = backend.run(circ, shots=4096, seed_simulator=12345)
result = job.result()
counts = result.get_counts()
print(counts)
