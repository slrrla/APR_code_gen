from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import device as noise_device
from qiskit.test.mock import FakeMelbourne

# Use a local mock backend instead of contacting a real IBMQ device
backend = FakeMelbourne()
properties = backend.properties()

# Build the approximate noise model from the (mock) device properties
noise_model = noise_device.basic_device_noise_model(properties)

# Simple circuit that only touches qubit 0, leaving qubit 1 idle
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

simulator = QasmSimulator()
result = execute(qc, backend=simulator, noise_model=noise_model, shots=1024).result()
print(result.get_counts())
