from qiskit import QuantumCircuit, __version__
from qiskit.quantum_info import StabilizerState

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(1, 2)

stab = StabilizerState(qc)
print(stab)
print("qiskit ver", __version__)
