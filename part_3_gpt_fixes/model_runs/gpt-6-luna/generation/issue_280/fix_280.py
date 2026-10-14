from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

noise_model = NoiseModel()

error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# FIX: the one-qubit error is incompatible with the two-qubit cx gate -> use a two-qubit depolarizing error, because the error dimension must match the gate's qubit count
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.05, 2), ['cx'])

print(noise_model)
