from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.quantum_info.states import partial_trace

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

traced_over = list(range(0, num_qubits))
traced_over.remove(3)
traced_over.remove(5)

rho = DensityMatrix.from_instruction(measureZZ)
rho_3_5 = partial_trace(rho, traced_over)

# Second Renyi entropy uses Tr(rho^2), which equals the purity
purity = rho_3_5.purity()
