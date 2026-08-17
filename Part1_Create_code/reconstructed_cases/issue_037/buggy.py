import numpy as np
from qiskit.aqua.input import EnergyInput

n = 2  # dimension of each data point

# Minimal synthetic dataset standing in for Breast_cancer()
training_input = {'A': np.random.rand(5, n), 'B': np.random.rand(5, n)}
test_input = {'A': np.random.rand(2, n), 'B': np.random.rand(2, n)}

temp = [test_input[k] for k in test_input]
total_array = np.concatenate(temp)

# Bug: EnergyInput expects an operator object, not a string label.
# This raises AttributeError: 'str' object has no attribute 'to_dict'
algo_input = EnergyInput('SVMInput')
algo_input.training_dataset = training_input
algo_input.test_dataset = test_input
algo_input.datapoints = total_array
