import numpy as np
from qiskit import QuantumCircuit
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.algorithms import IterativeAmplitudeEstimation, EstimationProblem, FasterAmplitudeEstimation

# simple state preparation circuit representing operator A
myqc = QuantumCircuit(1)
myqc.h(0)

problem = EstimationProblem(state_preparation=myqc, objective_qubits=[0])

backend = Aer.get_backend('aer_simulator')
quantum_instance = QuantumInstance(backend, shots=1000)

kwargs = {'epsilon_target': 0.01, 'alpha': 0.05, 'quantum_instance': quantum_instance}
algorithm = IterativeAmplitudeEstimation(**kwargs)
result = algorithm.estimate(problem)
amplitude = result.estimation
print(amplitude)
