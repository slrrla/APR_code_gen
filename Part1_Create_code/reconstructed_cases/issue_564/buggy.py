from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator, noise
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.fake_provider import FakeCairo

# Simple circuit to run
qc_combine = QuantumCircuit(2)
qc_combine.h(0)
qc_combine.cx(0, 1)
qc_combine.measure_all()

shots_done = 1024

prob_1 = 0.001  # 1-qubit gate
prob_2 = 0.01   # 2-qubit gate

# Depolarizing quantum errors
error_1 = noise.depolarizing_error(prob_1, 1)  # I think, one means here 1 qubit
error_2 = noise.depolarizing_error(prob_2, 2)  # I think, two means here 2 qubit

# Add errors to noise model
noise_model = noise.NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1, ['u1', 'u2', 'u3', 'x', 'y', 'z', 'h', 's', 't'])
noise_model.add_all_qubit_quantum_error(error_2, ['cx', 'cy', 'cz', 'swap'])

# Get basis gates from noise model
basis_gates = noise_model.basis_gates

# provider = IBMQ.load_account()
# using a local fake backend instead of a real hardware provider call
backend_cairo = FakeCairo()

# this overwrites the carefully constructed noise_model above,
# discarding the manually added errors
noise_model = NoiseModel.from_backend(backend_cairo)

# Get coupling map from backend
coupling_map = backend_cairo.configuration().coupling_map

# Perform a noise simulation
backend = AerSimulator(noise_model=noise_model, coupling_map=coupling_map, basis_gates=basis_gates)
transpiled_circuit = transpile(qc_combine, backend)
result = backend.run(transpiled_circuit, shots=shots_done).result()
print(result.get_counts())
