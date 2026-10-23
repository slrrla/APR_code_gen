from qiskit_aer.noise import NoiseModel
# FIX: backend was undefined and live-device access was restricted -> import a snapshot backend, because it requires no IBM device access.
from qiskit_ibm_runtime.fake_provider import FakeWashingtonV2

# FIX: no backend was supplied -> instantiate the 127-qubit Washington snapshot, because its stored calibration data supports noise-model construction.
backend = FakeWashingtonV2()
noise_model = NoiseModel.from_backend(backend)

