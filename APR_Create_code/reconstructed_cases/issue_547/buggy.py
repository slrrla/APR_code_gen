from qiskit import QuantumCircuit
import numpy as np

# Minimal reproduction of qc.unitary usage referenced in the question.
# The question is purely conceptual (asking which decomposition algorithm
# qc.unitary uses); no actual bug is present in the code itself.
qc = QuantumCircuit(2)
unitary_matrix = np.eye(4)  # placeholder unitary
qc.unitary(unitary_matrix, [0, 1])
print(qc.decompose())
