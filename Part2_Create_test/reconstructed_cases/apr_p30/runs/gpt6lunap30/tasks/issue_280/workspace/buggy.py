from qiskit_aer.noise import NoiseModel, depolarizing_error

# Create an empty noise model
noise_model = NoiseModel()

# Add depolarizing error to all single qubit u1, u2, u3 gates
error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# Apply a two-qubit depolarizing error to the 2-qubit CNOT gate.
cx_error = depolarizing_error(0.05, 2)
noise_model.add_all_qubit_quantum_error(cx_error, ['cx'])

# Print noise model info
print(noise_model)
