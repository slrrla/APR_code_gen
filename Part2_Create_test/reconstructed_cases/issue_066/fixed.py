from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Corrected method name casing ("statevector") and use device="CPU"
# so the circuit runs on the local simulator without requiring GPU hardware.
backend = AerSimulator(method="statevector", device="CPU")

# Create a simple quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Compile the circuit
qc = transpile(qc, backend)

# Execute the circuit
result = backend.run(qc).result()

# Show the probability
print(result.get_counts())
