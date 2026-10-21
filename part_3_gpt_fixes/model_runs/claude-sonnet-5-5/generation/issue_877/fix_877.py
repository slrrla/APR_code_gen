from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke

# FIX: `backend` was never defined -> create a fake backend from a stored snapshot of a large IBM device, because NoiseModel.from_backend needs a backend object and fake backends need no device access
backend = FakeSherbrooke()

noise_model = NoiseModel.from_backend(backend)
