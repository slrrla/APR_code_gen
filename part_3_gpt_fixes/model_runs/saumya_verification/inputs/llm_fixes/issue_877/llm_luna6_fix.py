from qiskit_aer.noise import NoiseModel

# FIX: `backend` was undefined -> use a bundled 27-qubit backend snapshot, because it provides an offline noise model without access to the live device
from qiskit.providers.fake_provider import FakeMontreal
backend = FakeMontreal()

noise_model = NoiseModel.from_backend(backend)

