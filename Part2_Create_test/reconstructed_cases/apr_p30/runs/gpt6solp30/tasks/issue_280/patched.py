from qiskit_aer.noise import NoiseModel, depolarizing_error

# Create an empty noise model
noise_model = NoiseModel()

# Add depolarizing error to all single qubit u1, u2, u3 gates
error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# A CNOT is a two-qubit gate, so its error must also act on two qubits.
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.05, 2), ['cx'])

# Print noise model info
print(noise_model)
