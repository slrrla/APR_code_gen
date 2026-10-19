from qiskit import BasicAer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.utils import split_dataset_to_data_and_labels
from qiskit.circuit.library import ZZFeatureMap
from qiskit.ml.datasets import breast_cancer

# Reduced training/test sizes so the run completes quickly,
# and feature map hyperparameters (reps, entanglement) tuned
# to trade off overfitting vs. generalization
training_size = 20
test_size = 10
n = 2  # number of features/qubits

sample_Total, training_input, test_input, class_labels = breast_cancer(
    training_size=training_size,
    test_size=test_size,
    n=n
)

feature_map = ZZFeatureMap(feature_dimension=n, reps=1, entanglement='linear')

backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1024)

qsvm = QSVM(feature_map, training_input, test_input)
result = qsvm.run(quantum_instance)

print("Testing success ratio:", result['testing_accuracy'])
