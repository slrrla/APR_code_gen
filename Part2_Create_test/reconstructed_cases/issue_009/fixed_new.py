#original question was:TranspilerError: Invalid layout method csp_layout

from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

coupling_map = [
    [0, 1], [1, 0],
    [1, 2], [2, 1],
]

# In Qiskit <= 0.23 / Terra 0.16,
# optimization_level >= 2 automatically tries CSPLayout first.
transpiled = transpile(
    qc,
    coupling_map=coupling_map,
    optimization_level=3,
)

print(transpiled)