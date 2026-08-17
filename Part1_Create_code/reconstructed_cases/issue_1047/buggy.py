import numpy as np
from dataset import breast_cancer
from qiskit.aqua.utils import split_dataset_to_data_and_labels
from qiskit.aqua.components.feature_maps import SecondOrderExpansion
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua import QuantumInstance
from qiskit import BasicAer

n = 2  # number of principal components kept
training_dataset_size = 20
testing_dataset_size = 10

# Only the built-in breast_cancer dataset generator is used here - there is
# no way to load a user's own .csv file into training_input / test_input.
sample_Total, training_input, test_input, class_labels = breast_cancer(
    training_dataset_size, testing_dataset_size, n)

data_train, _ = split_dataset_to_data_and_labels(training_input)
data_test, _ = split_dataset_to_data_and_labels(test_input)

feature_map = SecondOrderExpansion(feature_dimension=n, depth=1)
qsvm = QSVM(feature_map, training_input, test_input)

backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1024,
                                    seed_simulator=10598, seed_transpiler=10598)
result = qsvm.run(quantum_instance)

print("testing success ratio: ", result['testing_accuracy'])
