from qiskit_aer.noise import NoiseModel, depolarizing_error

# Parameters
p = 0.01
i, j = 0, 1

noise_model = NoiseModel()

# Model a noisy CNOT with a proper two-qubit depolarizing error channel,
# which is not the same as tensoring two independent single-qubit errors.
error = depolarizing_error(p, 2)
noise_model.add_quantum_error(error, ['cx'], [i, j])
