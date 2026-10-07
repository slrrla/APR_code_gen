from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, DiagonalGate

# Desired marked (solution) states for the oracle
targets = ['101', '110']

# BUG: Statevector.from_label only accepts a single bitstring label,
# not a list of multiple target states, so this does not build the
# intended oracle marking both |101> and |110>.
n = len(targets[0])
phases = [-1 if format(k, f'0{n}b') in targets else 1 for k in range(2**n)]
oracle = QuantumCircuit(n)
oracle.append(DiagonalGate(phases), range(n))

grover_op = GroverOperator(oracle)
print(grover_op)
