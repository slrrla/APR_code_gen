# imports
from qiskit import transpile
from qiskit.quantum_info import DensityMatrix, state_fidelity
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

# local stand-in for a real backend (no network calls)
backend = FakeBrisbane()
noise_model = NoiseModel.from_backend(backend)
simulator = AerSimulator(noise_model=noise_model)

# Create circuit and ideal state
qc = QFT(6)
rho_ideal = DensityMatrix(qc)
qc.save_density_matrix()

# Transpile and simulate noisy state
qc_t = transpile(qc, simulator)
rho_real = simulator.run(qc_t).result().data()['density_matrix']

# Compare
fidelity = state_fidelity(rho_ideal, rho_real)
print(f"Fidelity tra stato ideale e rumoroso: {fidelity:.4f}")
