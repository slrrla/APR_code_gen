from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

noise_model = NoiseModel()

error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# FIX: the CX instruction acts on two qubits -> create a two-qubit depolarizing error, because quantum error dimensions must match instruction qubits
error = depolarizing_error(0.05, 2)
noise_model.add_all_qubit_quantum_error(error, ['cx'])

print(noise_model)

