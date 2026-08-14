import qiskit
from qiskit.quantum_info import DensityMatrix

circuit = qiskit.QuantumCircuit(1, 1)
print(DensityMatrix.from_instruction(circuit))

circuit.measure(0, 0)
print(DensityMatrix.from_instruction(circuit))
