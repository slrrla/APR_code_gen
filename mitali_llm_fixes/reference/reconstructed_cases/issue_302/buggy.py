# User only knew about qiskit fake backends in general, no working
# selection strategy -- naive approach: just grab an arbitrary fake
# backend without checking its noise characteristics.
from qiskit_ibm_runtime import fake_provider

backend = fake_provider.FakeVigo()
print(f"Using backend: {backend.name}, n_qubits: {backend.configuration().n_qubits}")
