from qiskit_aer.noise import NoiseModel
# FIX: `backend` was undefined -> import a fake 27-qubit IBM backend snapshot, because the user has no access to the large device and NoiseModel.from_backend needs a backend object with calibration data
from qiskit_ibm_runtime.fake_provider import FakeMontreal

# FIX: `backend` was undefined -> instantiate the fake backend, because it supplies the device properties used to build the noise model
backend = FakeMontreal()

noise_model = NoiseModel.from_backend(backend)
