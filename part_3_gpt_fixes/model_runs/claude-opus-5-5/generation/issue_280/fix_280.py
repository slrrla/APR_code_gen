# FIX: deprecated/removed module path qiskit.providers.aer -> qiskit_aer, because Aer now lives in the separate qiskit_aer package
from qiskit_aer.noise import NoiseModel, depolarizing_error

noise_model = NoiseModel()

error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# FIX: 1-qubit error applied to 2-qubit 'cx' -> use a 2-qubit depolarizing_error, because the error's qubit count must match the gate's
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.05, 2), ['cx'])

print(noise_model)
