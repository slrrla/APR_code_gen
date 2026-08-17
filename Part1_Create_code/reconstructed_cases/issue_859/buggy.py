# Reproduces the reported problem: trying to implement the projector
# pi = [[1,0],[0,0]] on qubit 0 of a Bell state using the reset gate.
# Instead of always collapsing to |00>, the reset gate randomly gives
# |00> or |01> because it only zeroes the target qubit without
# properly renormalizing/projecting the joint state.

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Bell state |psi> = (|00> + |11>)/sqrt(2)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Attempt to apply the projector pi to qubit 0 using reset
qc.reset(0)

statevector = Statevector(qc)
print(statevector)
