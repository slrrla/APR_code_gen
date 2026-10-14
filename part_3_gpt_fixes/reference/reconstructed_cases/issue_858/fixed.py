from qiskit.providers.fake_provider import FakeOslo

# Use the fake backend snapshot to recover documented properties
# of the retired ibm_oslo system.
backend = FakeOslo()

# Single qubit properties
print(backend.qubit_properties(0))

# Properties for multiple qubits
print(backend.qubit_properties(range(7)))

# Extract just the T1 times
t1s = [prop.t1 for prop in backend.qubit_properties(range(7))]
print(t1s)
