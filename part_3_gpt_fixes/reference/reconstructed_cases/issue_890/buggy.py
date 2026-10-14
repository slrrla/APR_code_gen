from qiskit_aer.noise import NoiseModel, pauli_error

# Parameters
p = 0.01
i, j = 0, 1

noise_model = NoiseModel()

# Model a noisy CNOT as the tensor product of two independent
# single-qubit i.i.d. Pauli error channels (one per qubit).
error = pauli_error([('I', 1 - 3 * p), ('X', p), ('Y', p), ('Z', p)])
error = error.tensor(error)
noise_model.add_quantum_error(error, ['cx'], [i, j])
