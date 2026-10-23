from qiskit_aer.noise import NoiseModel
# FIX: backend was undefined and live-device access was unavailable -> import an offline IBM device snapshot, because it provides calibration data without device access.
from qiskit.providers.fake_provider import FakeWashington

# FIX: no backend was supplied -> instantiate the 127-qubit snapshot backend, because NoiseModel.from_backend can extract its stored noise parameters.
backend = FakeWashington()
noise_model = NoiseModel.from_backend(backend)

