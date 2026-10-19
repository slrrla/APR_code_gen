import numpy as np
from qiskit.providers.aer.noise import NoiseModel

# 2x2 readout probability matrix, built up element by element
probabilities = [None, None]
probabilities[0] = [0.9, 0.15]
probabilities[1] = [0.1, 0.85]

readout_noise_model = NoiseModel()
# FIX: pass the whole probability matrix in a single call
readout_noise_model.add_readout_error(probabilities, [0])
