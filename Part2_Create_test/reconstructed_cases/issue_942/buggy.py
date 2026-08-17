from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

AND = Operator([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0],
])

circ = QuantumCircuit(3)
circ.unitary(AND, [0, 1, 2], label="AND")

# After transpiling, the AND unitary loses its semantic meaning:
# the decomposed circuit just shows generic "circuit-XXX" gates
# instead of a recognizable Toffoli/AND structure.
decomposed = transpile(circ, basis_gates=["cx", "u"])
print(decomposed)
