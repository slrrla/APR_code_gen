from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

noise_model = NoiseModel()

error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# FIX: 1-qubit depolarizing error was applied to the 2-qubit 'cx' gate -> defined a 2-qubit depolarizing error for it, because cx acts on two qubits and needs a matching 2-qubit error
error_2q = depolarizing_error(0.05, 2)
# FIX: 1-qubit error was used for 'cx' -> use the 2-qubit error_2q, because the error's qubit count must match the gate's qubit count
noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

print(noise_model)
