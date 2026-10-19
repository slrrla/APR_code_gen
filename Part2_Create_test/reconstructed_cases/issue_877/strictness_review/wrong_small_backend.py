from qiskit.providers.fake_provider import FakeManila
from qiskit_aer.noise import NoiseModel

backend = FakeManila()
noise_model = NoiseModel.from_backend(backend)
