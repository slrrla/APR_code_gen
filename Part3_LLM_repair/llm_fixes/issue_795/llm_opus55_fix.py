import numpy as np
from qiskit import QuantumCircuit
# FIX: opflow PauliSumOp (removed API, appended as non-gate Instruction) -> SparsePauliOp from quantum_info, because it builds the same operator and can be turned into a matrix for a UnitaryGate
from qiskit.quantum_info import SparsePauliOp
I, X, Y, Z = (SparsePauliOp(p) for p in 'IXYZ')

circuit = QuantumCircuit(1, name='R')
# FIX: appending the operator object created a non-gate sub-circuit instruction -> append its matrix via circuit.unitary, because a UnitaryGate is a Gate so to_gate() succeeds
circuit.unitary((0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix(), [0])
circuit.to_gate()
