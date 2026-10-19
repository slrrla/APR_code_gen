from qiskit.providers.fake_provider import FakeWashington
from qiskit_aer.noise import NoiseModel

backend = FakeWashington()
noise_model = NoiseModel.from_backend(backend)
