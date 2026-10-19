import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit.circuit import Parameter
from qiskit_aer.noise import (
    NoiseModel,
    thermal_relaxation_error,
)

# --- Noise Model ---
T1 = 100e3  # ns
T2 = 200e3  # ns
time_ry = 200e3
errors_ry = [
    thermal_relaxation_error(T1, T2, time_ry)
]
noise_thermal = NoiseModel(basis_gates=['ry'])
noise_thermal.add_quantum_error(thermal_relaxation_error(T1, T2, time_ry), 'ry', [0])

sim_noisy = AerSimulator(noise_model=noise_thermal)
passmanager = generate_preset_pass_manager(
    optimization_level=0, backend=sim_noisy
)

# --- Circuit ---
circuit = QuantumCircuit(1, 1)
theta = Parameter('theta')
circuit.ry(theta, 0)
circuit.measure(0, 0)

circuit_transpiled = passmanager.run(circuit)

nshots = 4000

# Run and get counts
res = []
for th in np.linspace(0, 2*np.pi, 100):
    passmanager = generate_preset_pass_manager(
        optimization_level=0, backend=sim_noisy
    )
    circuit_transpiled = passmanager.run(circuit.assign_parameters({theta: th}))
    result_noisy = sim_noisy.run(circuit_transpiled, shots=nshots).result()
    counts_noisy = result_noisy.get_counts(0)
    if '1' not in counts_noisy:
        counts_noisy['1'] = 0
    res.append(counts_noisy['1'] / nshots)

plt.plot(res)
