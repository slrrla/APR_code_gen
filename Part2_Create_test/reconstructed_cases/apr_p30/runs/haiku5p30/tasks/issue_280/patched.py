from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

# Create an empty noise model
noise_model = NoiseModel()

# Add depolarizing error to all single qubit u1, u2, u3 gates
error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# Apply a 2-qubit depolarizing error to the 2-qubit CNOT gate
error_2q = depolarizing_error(0.05, 2)
noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

# Print noise model info
print(noise_model)
