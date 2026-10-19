from qiskit_aer.noise import NoiseModel
# FIX: A restricted live backend cannot be loaded -> import FakeWashington, because its 127-qubit device snapshot requires no IBM account access.
from qiskit.providers.fake_provider import FakeWashington

# FIX: backend was undefined -> instantiate FakeWashington, because its stored calibration data can supply the noise model.
backend = FakeWashington()
noise_model = NoiseModel.from_backend(backend)
