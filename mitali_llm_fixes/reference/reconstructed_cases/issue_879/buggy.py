from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

num_qubits = 12
measureZZ = QuantumCircuit(num_qubits, num_qubits)
measureZZ.h(0)
measureZZ.h(1)
measureZZ.h(5)
measureZZ.h(6)
measureZZ.cx(0, 2)
measureZZ.cx(1, 3)
measureZZ.cx(5, 7)
measureZZ.cx(6, 8)
measureZZ.cx(0, 3)
measureZZ.cx(1, 4)
measureZZ.cx(5, 8)
measureZZ.cx(6, 9)
measureZZ.cx(2, 5)
measureZZ.cx(4, 6)
measureZZ.cx(7, 10)
measureZZ.cx(9, 11)

# Trying to get the state of a subsystem (qubits 3 and 5) using Statevector,
# which fails because the subsystem may be entangled with the rest.
sv = Statevector.from_instruction(measureZZ)
# No proper way to reduce Statevector to a subsystem - this is the bug.
rho_3_5 = sv  # incorrect: should use partial_trace on a DensityMatrix instead
