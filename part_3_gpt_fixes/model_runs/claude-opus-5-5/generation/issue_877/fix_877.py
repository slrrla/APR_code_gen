from qiskit_aer.noise import NoiseModel
# FIX: backend was never defined (no access to large real devices) -> import a fake snapshot of a large IBM device, because fake backends carry the real device's calibration/noise data
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke

# FIX: undefined name `backend` -> instantiate the fake 127-qubit backend, because NoiseModel.from_backend needs an actual backend object
backend = FakeSherbrooke()
noise_model = NoiseModel.from_backend(backend)
