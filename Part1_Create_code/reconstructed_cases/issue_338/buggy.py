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

# default statevector-based simulator - runs out of memory / too many
# subscripts in einsum for large n
simulator = AerSimulator()
result = simulator.run(qc, shots=1).result()
counts = result.get_counts()
print(counts)
