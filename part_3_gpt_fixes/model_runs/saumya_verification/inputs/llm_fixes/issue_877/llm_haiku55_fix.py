# FIX: `backend` was never defined (NameError) and the real device is inaccessible -> import an offline fake 127-qubit backend snapshot and assign it to `backend`, because it provides the device's calibration data without needing access
from qiskit_ibm_runtime.fake_provider import FakeWashingtonV2
backend = FakeWashingtonV2()
from qiskit_aer.noise import NoiseModel

noise_model = NoiseModel.from_backend(backend)
