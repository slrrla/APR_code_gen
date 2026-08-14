from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.providers.fake_provider import GenericBackendV2

device_backend = GenericBackendV2(num_qubits=10)
device_backend.target['id'][(0,)].error = 1
backend = AerSimulator.from_backend(device_backend)

# Create a simple circuit
circuit = QuantumCircuit(3)
circuit.id(0)
circuit.measure_all()
circuit.draw('mpl')

# Execute noisy simulation and get counts
result_noise = backend.run(circuit).result()  # Use the original circuit here
counts_noise = result_noise.get_counts(0)
plot_histogram(counts_noise, title="title")
