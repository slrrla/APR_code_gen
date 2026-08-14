import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

# --- Parameters ---
T1 = 10e3  # ns (relaxation time)
T2 = 20e3
time_step = 50  # ns (discretization step for the rotation)
nshots = 200

# Noise model
noise_model = NoiseModel()
error = thermal_relaxation_error(T1, T2, time_step)
noise_model.add_all_qubit_quantum_error(error, 'ry')  # Add to idle operations

# Simulator
simulator = AerSimulator(noise_model=noise_model)

# --- Circuit Construction ---
n_steps = 300  # Number of steps to discretize the Rabi oscillation
theta = np.pi / 50
results = []

for step in range(1, n_steps + 1):
    circuit = QuantumCircuit(1, 1)
    for _ in range(step):
        circuit.ry(theta, 0)
    circuit.measure(0, 0)

    transpiled_circuit = transpile(circuit, simulator)
    result = simulator.run(transpiled_circuit, shots=nshots).result()
    counts = result.get_counts()
    prob_1 = counts.get('1', 0) / nshots
    results.append(prob_1)

# --- Plot Results ---
time = np.linspace(0, n_steps * time_step, n_steps)  # Time axis in ns
plt.plot(time, results, label="Simulated Rabi Oscillations (damped)")
plt.xlabel('Time (ns)')
plt.ylabel('Excitation Probability')
plt.title('Rabi Oscillations with Decoherence')
plt.legend()
plt.grid()
plt.show()
