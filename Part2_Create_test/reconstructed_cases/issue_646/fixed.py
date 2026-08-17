import numpy as np
from qiskit import Aer
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.algorithms.optimizers import COBYLA
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.algorithms.classifiers import VQC

num_inputs = 2
num_samples = 100
X = 2 * np.random.rand(num_samples, num_inputs) - 1
y = np.random.choice([0, 1, 2, 3], num_samples)
y_one_hot = np.zeros((num_samples, 4))
for i in range(len(y)):
    y_one_hot[i, y[i]] = 1

feature_map = ZZFeatureMap(num_inputs)
ansatz = RealAmplitudes(num_inputs, reps=1)

vqc = VQC(
    feature_map=feature_map,
    ansatz=ansatz,
    loss='cross_entropy',
    optimizer=COBYLA(),
    quantum_instance=QuantumInstance(Aer.get_backend('qasm_simulator')),
)

# Fix: the nan-loss issue when fitting VQC with multi-class (one-hot)
# labels was a bug in qiskit_machine_learning 0.3.0. It was resolved in
# the 0.4.0 development version, installed from a clone of the repo via:
#   pip install .
# No changes to this script itself are required once the fixed library
# version is installed.
vqc.fit(X, y_one_hot)
print(vqc.weights)
