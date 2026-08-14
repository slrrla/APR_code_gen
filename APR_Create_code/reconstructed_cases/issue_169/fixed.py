from qiskit import QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info.synthesis.two_qubit_decompose import TwoQubitBasisDecomposer
from qiskit.extensions.quantum_initializer.isometry import Isometry
import qiskit.quantum_info.synthesis.qsd as qsd
import numpy as np

# For 2x2 unitaries, UnitaryGate just emits a U3 gate.
# For 4x4 unitaries, TwoQubitBasisDecomposer (KAK decomposition) is used,
# giving the optimal number of CNOT gates.
# For larger unitaries, Isometry is used (Iten et al. method).
# Since Qiskit 0.37, qiskit.quantum_info.synthesis.qsd implements
# Quantum Shannon Decomposition, using about half the CNOTs of the
# isometry-based approach for unitaries on more than two qubits.

unitary_matrix = np.array([[1, 0], [0, 1]])  # placeholder 2x2 unitary

qc = QuantumCircuit(1)
gate = UnitaryGate(unitary_matrix)
qc.append(gate, [0])

print(qc.decompose())
