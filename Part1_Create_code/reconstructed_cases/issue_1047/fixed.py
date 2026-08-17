import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

from qiskit.aqua.components.feature_maps import SecondOrderExpansion
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua import QuantumInstance
from qiskit import BasicAer

n = 2  # number of principal components kept
training_dataset_size = 20
testing_dataset_size = 10


def load_data(location, file):
    """Load a user-provided .csv file. The last column is treated as
    the class label, all other columns are treated as features."""
    df = pd.read_csv(location + file)
    target_names = df.iloc[:, -1].unique()
    target = df.iloc[:, -1].values
    data = df.iloc[:, :-1].values
    return data, target, target_names


def userDefinedData(location, file, class_labels, training_size, test_size,
                     n=2, PLOT_DATA=True):
    data, target, target_names = load_data(location, file)
    # sample_train is of the same form as data
    sample_train, sample_test, label_train, label_test = train_test_split(
        data, target, test_size=0.25, train_size=0.75, random_state=22)

    # Now we standarize for gaussian around 0 with unit variance
    std_scale = StandardScaler().fit(sample_train)
    sample_train = std_scale.transform(sample_train)
    sample_test = std_scale.transform(sample_test)

    # Now reduce number of features to number of qubits
    pca = PCA(n_components=n).fit(sample_train)
    sample_train = pca.transform(sample_train)
    sample_test = pca.transform(sample_test)

    # Samples are pairs of points
    samples = np.append(sample_train, sample_test, axis=0)
    minmax_scale = MinMaxScaler((-1, 1)).fit(samples)
    sample_train = minmax_scale.transform(sample_train)
    sample_test = minmax_scale.transform(sample_test)

    # If class labels are numeric
    if class_labels[0].isdigit():
        # Pick training size number of samples from each distro
        training_input = {key: (sample_train[label_train == int(key), :])[:training_size]
                           for k, key in enumerate(class_labels)}
        test_input = {key: (sample_test[label_test == int(key), :])[:test_size]
                       for k, key in enumerate(class_labels)}
    else:
        # if they aren't
        training_input = {key: (sample_train[label_train == k, :])[:training_size]
                           for k, key in enumerate(class_labels)}
        test_input = {key: (sample_train[label_train == k, :])[training_size:(training_size + test_size)]
                      for k, key in enumerate(class_labels)}

    if PLOT_DATA:
        for k in range(0, 9):
            plt.scatter(sample_train[label_train == k, 0][:training_size],
                        sample_train[label_train == k, 1][:training_size])
        plt.title("PCA dim. reduced user dataset")
        plt.show()

    return sample_train, training_input, test_input, class_labels


class_labels = ['0', '1']
sample_Total, training_input, test_input, class_labels = userDefinedData(
    './', 'my_data.csv', class_labels, training_dataset_size,
    testing_dataset_size, n, PLOT_DATA=False)

feature_map = SecondOrderExpansion(feature_dimension=n, depth=1)
qsvm = QSVM(feature_map, training_input, test_input)

backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1024,
                                    seed_simulator=10598, seed_transpiler=10598)
result = qsvm.run(quantum_instance)

print("testing success ratio: ", result['testing_accuracy'])
