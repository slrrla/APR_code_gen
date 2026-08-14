from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, StabilizerState
from qiskit.visualization import array_to_latex

qc = QuantumCircuit(2)
rho = DensityMatrix(qc)

qc.h(0)
qc.x(1)

stabstate = StabilizerState(qc)
rho = rho.evolve(stabstate)

array_to_latex(rho)
