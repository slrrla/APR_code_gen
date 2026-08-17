from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Attempt to use GPU-backed AerSimulator, as reported by the user.
# NOTE: method casing is "Statevector" (capitalized) exactly as the user typed it,
# and device="GPU" is requested even though no CUDA device is available in this environment.
backend = AerSimulator(method="Statevector", device="GPU")

# Create a simple quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Compile the circuit
qc = transpile(qc, backend)

# Execute the circuit -- this raises RuntimeError: No CUDA device available!
result = backend.run(qc).result()

# Show the probability
print(result.get_counts())
