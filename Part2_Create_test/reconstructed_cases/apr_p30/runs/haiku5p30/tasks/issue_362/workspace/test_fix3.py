from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Simple circuit without classical register
circuit = QuantumCircuit(1)
circuit.h(0)

# Let's see what options are available for AerSimulator
backend = AerSimulator(method='unitary')
print("Backend name:", backend.name)
print("Backend options:", backend.options)

# Try with save_unitary
circuit2 = QuantumCircuit(1)
circuit2.h(0)
circuit2.save_unitary()

job2 = backend.run(circuit2).result()
print("\nWith save_unitary():")
print("Result dict data:", job2.data(0))
print("Result object:", job2.results[0])
