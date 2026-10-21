import numpy as np
from qiskit import QuantumCircuit
# FIX: opflow operators (removed in Qiskit 1.0) were used -> import quantum_info Operator, because it can be turned into a proper UnitaryGate
from qiskit.quantum_info import Operator

circuit = QuantumCircuit(1, name='R')
# FIX: appending a PauliSumOp created a non-gate "circuit-xxx" instruction -> build the Operator and add it with circuit.unitary, because a UnitaryGate is a Gate and to_gate() accepts it
circuit.unitary(0.5*Operator.from_label('I') - 1j*np.sqrt(1-0.5**2)*Operator.from_label('Y'), [0])
circuit.to_gate()
