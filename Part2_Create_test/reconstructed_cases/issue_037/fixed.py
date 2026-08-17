import numpy as np
from qiskit.aqua.input import ClassificationInput

n = 2  # dimension of each data point

# Minimal synthetic dataset standing in for Breast_cancer()
training_input = {'A': np.random.rand(5, n), 'B': np.random.rand(5, n)}
test_input = {'A': np.random.rand(2, n), 'B': np.random.rand(2, n)}

temp = [test_input[k] for k in test_input]
total_array = np.concatenate(temp)
datapoints = [total_array]

# Fix: use ClassificationInput, passing the datasets and datapoints directly.
algo_input = ClassificationInput(training_input, test_input, datapoints[0])
