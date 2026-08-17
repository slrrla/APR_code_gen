import numpy as np
from qiskit.circuit.library import ZFeatureMap
from qiskit.compiler.transpiler import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import PegasosQSVC

num_qubits = 2
C = 1.0
tau = 100

train_features = np.random.rand(10, num_qubits)
train_labels = np.random.choice([-1, 1], 10)
test_features = np.random.rand(5, num_qubits)
test_labels = np.random.choice([-1, 1], 5)

# use a local Aer simulator instead of a backend that enforces ISA constraints
backend = AerSimulator()

# importing feature map
# define feature map to be used in the algorithm
featuremap = ZFeatureMap(feature_dimension=num_qubits, reps=3)

# transpile the featuremap to make it compatible with the backend topology
transpiled_featuremap = transpile(circuits=featuremap, backend=backend)

# FIX: use the Sampler primitive from Aer, which runs locally and does not
# enforce the hardware ISA on the internally built fidelity circuit
sampler = Sampler()

# set the fidelity parameter
fidelity = ComputeUncompute(sampler=sampler)

# setting the kernel
qkernel = FidelityQuantumKernel(feature_map=transpiled_featuremap, fidelity=fidelity)

# fitting the classifier
pegasos = PegasosQSVC(quantum_kernel=qkernel, C=C, num_steps=tau)
pegasos.fit(train_features, train_labels)
pegasos_score = pegasos.score(test_features, test_labels)
print(f"Pegasosqsvc classification test score: {pegasos_score*100}")
