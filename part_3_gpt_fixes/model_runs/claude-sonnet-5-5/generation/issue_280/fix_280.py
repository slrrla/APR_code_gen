from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

noise_model = NoiseModel()

error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# FIX: 1-qubit error was applied to the 2-qubit 'cx' gate -> use a 2-qubit depolarizing error, because the error's qubit count must match the gate's qubit count
error_2q = depolarizing_error(0.05, 2)
noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

print(noise_model)
