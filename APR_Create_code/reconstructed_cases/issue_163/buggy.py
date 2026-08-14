import numpy as np
from qiskit import QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import Statevector

# State a|00> + b|01> + c|10> + d|11>
a, b, c, d = 0.5, 0.5, 0.5, 0.5
qc = QuantumCircuit(2)
qc.initialize([a, b, c, d], [0, 1])

# Attempt: reset qubit 0 to |0> and apply U, hoping to act only on the
# {|01>, |10>} subspace. This destroys the superposition instead of
# preserving it, since reset collapses the state.
qc.reset(0)

U = np.array([[0, 1],
              [1, 0]])
qc.append(UnitaryGate(U), [0])

sv = Statevector(qc)
print(sv)
