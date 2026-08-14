from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import Sampler
from qiskit_aer import AerSimulator
import time


def bernstein_vazirani_algorithm(n, marked_state):
    """Creates a Bernstein-Vazirani algorithm circuit for n qubits and a specified marked state."""
    qr = QuantumRegister(n + 1)  # Add an extra ancilla qubit
    cr = ClassicalRegister(n)  # Classical register for n bits
    qc = QuantumCircuit(qr, cr)
    # Step 1: Apply Hadamard gates to all input qubits (excluding ancilla)
    qc.h(qr[:-1])
    # Step 2: Put the ancilla in |-> state
    qc.x(qr[-1])
    qc.h(qr[-1])
    # Step 3: Apply CNOT gates to encode the hidden string
    for i in range(n):
        if marked_state[i] == '1':
            qc.cx(qr[i], qr[-1])  # Use ancilla as the target
    # Step 4: Apply Hadamard gates again to all input qubits (excluding ancilla)
    qc.h(qr[:-1])
    # Step 5: Measure the input qubits
    qc.measure(qr[:-1], cr)
    return qc


# Configuration
n = 3
marked_state = '101'

# Use a local simulator instead of a real IBM backend
backend = AerSimulator()
print(f"Using backend: {backend.name}")

# Create and transpile the Bernstein-Vazirani circuit
qc = bernstein_vazirani_algorithm(n, marked_state)
qc_transpiled = transpile(qc, backend)

# Use the Sampler primitive to execute the circuit
sampler = Sampler(mode=backend)
job = sampler.run([qc_transpiled], shots=1024)

# Get results and extract measurement data
result = job.result()
counts = result.quasi_dists[0].binary_probabilities()

# Print raw measurement counts
print("Raw Measurement Counts:", counts)

# Convert counts to probabilities
print("Measurement Results (Probabilities):", counts)

# Plot histogram of results
plot_histogram(counts)
