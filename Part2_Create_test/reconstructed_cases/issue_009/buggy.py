from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# Using an invalid layout method name causes a TranspilerError
transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    layout_method='csp_layout'
)

print(transpiled)
