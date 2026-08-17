from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
# Use a local fake backend that models ibm_brisbane instead of trying to
# fetch a real (or nonexistent) remote backend
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

# create a bell circuit
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])

# get a local fake backend that mirrors ibm_brisbane's properties
backend = FakeBrisbane()

# transpile to backend
circ = transpile(circuit, backend=backend)

# create a simulator based on the backend's noise model
sim = AerSimulator.from_backend(backend)

# simulate and extract results
simulator_result = sim.run(circ).result()
simulator_counts = simulator_result.get_counts()
print(simulator_counts)
