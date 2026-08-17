import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.providers.aer.noise import NoiseModel, QuantumError, ReadoutError

# Build GHZ circuit
circ = QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)

# Create measurement circuit
meas = QuantumCircuit(3, 3)
meas.barrier(range(3))
# map the quantum measurement to the classical bits
meas.measure(range(3), range(3))

# Compose the measurement circuit before the GHZ circuit
qc = meas.compose(circ, range(3), front=True)

# Create noise model
readout_noise_model = NoiseModel()

# Create the readout error matrix
P = np.array([[0.9,0.02,0.02,0.02,0.02,0.01,0.01,0.0],
              [0.02,0.9,0.02,0.02,0.02,0.01,0.01,0.0],
              [0.02,0.02,0.9,0.02,0.02,0.01,0.01,0.0],
              [0.02,0.02,0.02,0.9,0.02,0.01,0.01,0.0],
              [0.02,0.02,0.02,0.02,0.9,0.01,0.01,0.0],
              [0.02,0.02,0.02,0.01,0.01,0.9,0.01,0.01],
              [0.01,0.02,0.02,0.02,0.03,0.04,0.84,0.02],
              [0.02,0.02,0.02,0.02,0.04,0.04,0.04,0.8]])

# Add readout error to the qubits
readout_noise_model.add_readout_error(P, [0, 1, 2])
print(readout_noise_model)

backend = AerSimulator()

# Transpile the quantum circuit to the low-level instructions used by the backend
qc_compiled = transpile(qc, backend)

# Execute the circuit on the simulator with the noise model
job_sim = backend.run(qc_compiled, shots=1024, noise_model=readout_noise_model)

# Grab the results from the job
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)
print(counts)
