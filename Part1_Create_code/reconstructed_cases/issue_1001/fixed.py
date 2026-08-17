import warnings
warnings.filterwarnings('ignore')

from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import depolarizing_error, thermal_relaxation_error

myNoiseModel = NoiseModel()

error1 = depolarizing_error(0.001, 1)
error2 = thermal_relaxation_error(50, 30, 0.1)

# Use the NoiseModel's own 'warnings' parameter instead of the warnings module
myNoiseModel.add_quantum_error(error1, ['u2'], [0], warnings=False)
myNoiseModel.add_quantum_error(error2, ['u2'], [0], warnings=False)
