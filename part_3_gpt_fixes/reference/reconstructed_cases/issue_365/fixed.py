import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UCGate

n = 3
qc = QuantumCircuit(n)

U_0 = np.array([[1, 0], [0, 1]])

j = 0
uc_gate = UCGate(U_0, up_to_diagonal=True)
# define your quantum circuit here...
# then append the uc_gate using:
qc.append(uc_gate, qc.qubits[j:])

print(qc)
