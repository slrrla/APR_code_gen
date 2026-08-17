import numpy as np
from qiskit import QuantumCircuit, transpile
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

# number of iterations / oracle queries used by IAE
num_iterations = len(result.powers)
print("number of iterations:", num_iterations)

# inspect the per-iteration circuit results returned by the algorithm
print(result.circuit_results)

# get the actual problem circuit constructed internally
problem_circuit = algorithm.construct_circuit(problem)

# recommended way to view the problem gate
print(transpile(problem_circuit, basis_gates=['ry', 'cx', 'ccx', 'x']).draw())

# inspect all available attributes on the result object
print(dir(result))
