from qiskit.result import models
from qiskit.validation import base

raw_counts = {'0x0': 4, '0x2': 10}
# Wrap the dict in a base.Obj instance so it matches the expected schema
data = models.ExperimentResultData(counts=base.Obj(**raw_counts))
print(data)
