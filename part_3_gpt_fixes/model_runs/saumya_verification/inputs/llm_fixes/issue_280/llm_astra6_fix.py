from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

noise_model = NoiseModel()

error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# FIX: A one-qubit error was assigned to cx -> use a two-qubit depolarizing error, because cx acts on two qubits.
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.05, 2), ['cx'])

print(noise_model)

