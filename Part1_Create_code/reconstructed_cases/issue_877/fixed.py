from qiskit.providers.fake_provider import FakeKolkata
from qiskit_aer.noise import NoiseModel

backend = FakeKolkata()
noise_model = NoiseModel.from_backend(backend)
