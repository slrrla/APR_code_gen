from qiskit.providers.aer.noise import device
from qiskit.test.mock import FakeVigo

# Build a noise model from a backend's properties
backend = FakeVigo()
properties = backend.properties()

noise_model = device.basic_device_noise_model(properties)

# Print out the raw error parameters for inspection
for error in noise_model.to_dict()['errors']:
    print(error)
