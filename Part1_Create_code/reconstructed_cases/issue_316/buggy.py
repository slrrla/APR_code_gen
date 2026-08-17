from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Prepare the state |0+> : qubit 0 in |0>, qubit 1 in |+>
qc = QuantumCircuit(2)
qc.h(1)

# Buggy algebraic approach: the author factored the state and then
# applied the T-phase unconditionally to the target qubit, as if the
# control qubit being |0> still triggered the phase kickback.
qc.t(1)

state = Statevector.from_instruction(qc)
print(state)
