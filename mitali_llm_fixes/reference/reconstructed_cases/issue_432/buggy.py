import numpy as np
from qiskit.circuit.library import ZFeatureMap
from qiskit.compiler.transpiler import transpile
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import Sampler
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

# local fake backend that enforces ISA (basis gate) constraints, similar to a real IBM device
backend = FakeManilaV2()

# importing feature map
# define feature map to be used in the algorithm
featuremap = ZFeatureMap(feature_dimension=num_qubits, reps=3)

# transpile the featuremap to make it compatible with the backend topology
transpiled_featuremap = transpile(circuits=featuremap, backend=backend)

# set the sampler that will run the circuits on the backend
sampler = Sampler(mode=backend)

# set the fidelity parameter
# BUG: only the featuremap is transpiled for the target ISA; the fidelity
# (kernel) circuit built internally as circuit + circuit.inverse() is never
# re-transpiled, so it contains gates (e.g. sxdg) unsupported by the backend
fidelity = ComputeUncompute(sampler=sampler)

# setting the kernel
qkernel = FidelityQuantumKernel(feature_map=transpiled_featuremap, fidelity=fidelity)

# fitting the classifier
pegasos = PegasosQSVC(quantum_kernel=qkernel, C=C, num_steps=tau)
pegasos.fit(train_features, train_labels)
# raises: "The instruction sxdg on qubits (1,) is not supported by the target system."
pegasos_score = pegasos.score(test_features, test_labels)
print(f"Pegasosqsvc classification test score: {pegasos_score*100}")
