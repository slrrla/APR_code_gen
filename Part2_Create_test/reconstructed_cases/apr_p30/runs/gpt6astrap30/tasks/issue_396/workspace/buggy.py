from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate, GroverOperator

# Desired marked (solution) states for the oracle
targets = ['101', '110']

# Computational-basis indices follow Qiskit's bitstring ordering.
num_qubits = len(targets[0])
phases = [1] * (2 ** num_qubits)
for target in targets:
    phases[int(target, 2)] = -1
oracle = QuantumCircuit(num_qubits)
oracle.append(DiagonalGate(phases), range(num_qubits))

grover_op = GroverOperator(oracle)
print(grover_op)
