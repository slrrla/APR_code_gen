from qiskit_aer.noise import NoiseModel
# FIX: `backend` was never defined and the real large device is inaccessible -> import and instantiate a fake snapshot of a large IBM device, because fake backends carry real calibration data usable by NoiseModel.from_backend without account access
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
backend = FakeSherbrooke()

noise_model = NoiseModel.from_backend(backend)

