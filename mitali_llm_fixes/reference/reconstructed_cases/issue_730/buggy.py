# Attempting to use the qiskit_aer namespace directly (pre-0.11 style import)
# This fails with: ModuleNotFoundError: No module named 'qiskit_aer'
import qiskit_aer.noise as noise

# Build a simple noise model
noise_model = noise.NoiseModel()
