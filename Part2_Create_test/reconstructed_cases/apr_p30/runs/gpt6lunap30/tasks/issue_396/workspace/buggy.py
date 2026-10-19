from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate, GroverOperator

# Desired marked (solution) states for the oracle
targets = ['101', '110']

# Build a diagonal phase oracle that flips the phase of every target state.
phases = [1] * (1 << len(targets[0]))
for target in targets:
    phases[int(target, 2)] = -1

oracle = QuantumCircuit(len(targets[0]))
oracle.append(DiagonalGate(phases), range(oracle.num_qubits))

grover_op = GroverOperator(oracle)
print(grover_op)
