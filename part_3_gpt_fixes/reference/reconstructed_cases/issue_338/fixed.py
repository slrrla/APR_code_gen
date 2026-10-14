from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford
from qiskit_aer import AerSimulator

n = 40  # large number of qubits
qc = QuantumCircuit(n)

# apply a random Clifford operation across the whole register
cliff = random_clifford(n)
qc.append(cliff.to_circuit(), range(n))

# apply a single T-gate
qc.t(0)

qc.measure_all()

# use a simulator method designed for Clifford+T circuits with many qubits
# options: 'extended_stabilizer' or 'matrix_product_state'
simulator = AerSimulator(method='extended_stabilizer')
# simulator = AerSimulator(method='matrix_product_state')

result = simulator.run(qc, shots=1).result()
counts = result.get_counts()
print(counts)
