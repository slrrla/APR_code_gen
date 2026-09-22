from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.extensions import UnitaryGate

# Use isometry() instead of initialize(), since it does not
# apply an internal reset and can be turned into a controllable gate
state = [0.5, 0.5, 0.5, 0.5]

qc_iso = QuantumCircuit(2)
qc_iso.isometry(state, [0, 1], [])

controlled_gate = UnitaryGate(Operator(qc_iso)).control()
