# Legacy Qiskit Aer noise model example
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error

# Successfully implemented bit-flip / reset error using pauli_error
p_reset = 0.05
error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])

# Attempt to implement a kraus_error the same way, but kraus_error
# was never imported (user could not find how to import it),
# so this raises a NameError when the script runs.
kraus_matrices = [
    [[1, 0], [0, 0]],
    [[0, 0], [0, 1]],
]
error_kraus = kraus_error(kraus_matrices)

noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(error_reset, ['reset'])
noise_model.add_all_qubit_quantum_error(error_kraus, ['id'])

print(noise_model)
