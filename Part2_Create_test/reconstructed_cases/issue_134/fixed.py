from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import device as noise_device
from qiskit.test.mock import FakeMelbourne

# Use a local mock backend instead of contacting a real IBMQ device
backend = FakeMelbourne()
properties = backend.properties()

# Build the approximate noise model from the (mock) device properties
noise_model = noise_device.basic_device_noise_model(properties)

# The noise model only applies gate_error (relaxation + depolarizing) errors
# to qubits that participate in a gate. Idle qubits do not accrue any
# relaxation error unless an explicit "id" gate is scheduled on them.
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.id(1)  # explicitly account for the idle qubit's relaxation error
qc.measure([0, 1], [0, 1])

simulator = QasmSimulator()
result = execute(qc, backend=simulator, noise_model=noise_model, shots=1024).result()
print(result.get_counts())
