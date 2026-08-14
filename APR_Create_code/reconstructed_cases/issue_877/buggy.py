from qiskit_aer.noise import NoiseModel

# User does not have access to a real backend with more than 7 qubits,
# so 'backend' is undefined/unavailable in their environment.
noise_model = NoiseModel.from_backend(backend)
