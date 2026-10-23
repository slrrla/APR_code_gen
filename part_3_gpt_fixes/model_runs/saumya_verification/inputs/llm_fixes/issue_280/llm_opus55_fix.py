# FIX: removed module qiskit.providers.aer -> import from qiskit_aer.noise, because Aer now lives in the separate qiskit_aer package
from qiskit_aer.noise import NoiseModel, depolarizing_error

noise_model = NoiseModel()

error = depolarizing_error(0.05, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

# FIX: 1-qubit error applied to 2-qubit 'cx' gate -> use depolarizing_error(0.05, 2), because a cx error must act on 2 qubits (uniform over the 15 two-qubit Paulis)
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.05, 2), ['cx'])

print(noise_model)
