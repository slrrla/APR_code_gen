from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import TGate
import numpy as np

# Prepare the state |0+> : qubit 0 in |0>, qubit 1 in |+>
qc = QuantumCircuit(2)
qc.h(1)

# Correct approach: apply the controlled-T gate with qubit 0 as control.
# Since qubit 0 is |0>, the |1><1| ⊗ T term contributes nothing, so the
# state is unchanged, matching the Dirac-notation derivation.
ct = TGate().control(1)
qc.append(ct, [0, 1])

state = Statevector.from_instruction(qc)
print(state)
