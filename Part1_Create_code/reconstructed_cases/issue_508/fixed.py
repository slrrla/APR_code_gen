from qiskit.providers.aer.noise import device
from qiskit.test.mock import FakeVigo

# Build a noise model from a backend's properties
backend = FakeVigo()
properties = backend.properties()

noise_model = device.basic_device_noise_model(properties)

# Each entry in noise_model.to_dict()['errors'] is a QuantumError dict.
# 'instructions' is a list of possible error instructions (Kraus-like
# Pauli/reset operations) that can be applied on the qubits given by
# each instruction's 'qubits' field.
# 'probabilities' gives, in the same order, the probability that the
# corresponding entry in 'instructions' is applied instead of the
# ideal gate.
for error in noise_model.to_dict()['errors']:
    print("operations:", error['operations'])
    print("instructions:", error['instructions'])
    print("probabilities:", error['probabilities'])
