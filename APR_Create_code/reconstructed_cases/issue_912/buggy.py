from qiskit.result import models

raw_counts = {'0x0': 4, '0x2': 10}
# Attempting to pass a plain dict directly as counts data
data = models.ExperimentResultData(counts=raw_counts)
print(data)
