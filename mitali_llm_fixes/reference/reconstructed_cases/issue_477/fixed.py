# To emulate a processor with a specific (lower) quantum volume on the
# ideal qasm_simulator, you must explicitly constrain it with a noise
# model and a coupling map, then iterate on the noise parameters until
# the measured/estimated QV matches the desired value.

from qiskit import Aer, QuantumCircuit, execute
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

backend = Aer.get_backend('qasm_simulator')

# Restrict topology to force a lower effective quantum volume.
coupling_map = [[0, 1], [1, 2], [2, 3], [3, 4]]

# Add depolarizing noise to single- and two-qubit gates; tune these
# error rates and coupling map iteratively until the computed QV
# matches the target value (e.g. QV = 2^m for desired m < n_qubits).
noise_model = NoiseModel()
error_1q = depolarizing_error(0.001, 1)
error_2q = depolarizing_error(0.01, 2)
noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3'])
noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

qc = QuantumCircuit(5, 5)
qc.h(range(5))
qc.measure(range(5), range(5))

result = execute(
    qc,
    backend,
    coupling_map=coupling_map,
    noise_model=noise_model,
    shots=1024
).result()
print(result.get_counts())
