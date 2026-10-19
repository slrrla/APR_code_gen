import numpy as np
from qiskit import QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import Statevector

# State a|00> + b|01> + c|10> + d|11>
a, b, c, d = 0.5, 0.5, 0.5, 0.5
qc = QuantumCircuit(2)
qc.initialize([a, b, c, d], [0, 1])

U = np.array([[0, 1],
              [1, 0]])

# Step 1: permute basis states so that |01> -> |11> while |10> stays |10>
qc.cx(1, 0)

# Step 2: apply the single-qubit unitary on qubit 0, controlled on qubit 1
cu = UnitaryGate(U).control(1)
qc.append(cu, [1, 0])

# Step 3: undo the permutation from Step 1
qc.cx(1, 0)

sv = Statevector(qc)
print(sv)
