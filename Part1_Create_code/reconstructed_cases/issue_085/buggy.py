import numpy as np
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.algorithms.optimizers import ADAM
from qiskit_machine_learning.algorithms.classifiers import VQC

num_inputs = 2

# construct feature map, ansatz, and optimizer
feature_map = ZZFeatureMap(num_inputs)
ansatz = RealAmplitudes(num_inputs, reps=1)
optimizer = ADAM()  # no learning rate / tolerance set -> can't control iterations or lr

backend = Aer.get_backend('aer_simulator')
quantum_instance = QuantumInstance(backend, shots=1024)

def callback_graph(weights, obj_func_eval):
    pass

# construct variational quantum classifier
vqc = VQC(feature_map=feature_map,
          ansatz=ansatz,
          loss='cross_entropy',
          optimizer=optimizer,
          quantum_instance=quantum_instance,
          callback=callback_graph)

# toy training data
X = np.random.rand(4, num_inputs)
y = np.array([0, 1, 0, 1])

vqc.fit(X, y)
