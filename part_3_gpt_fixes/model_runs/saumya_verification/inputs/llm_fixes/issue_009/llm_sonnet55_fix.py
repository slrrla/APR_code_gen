from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# FIX: invalid layout_method='csp_layout' -> removed the argument, because CSP layout is not a selectable layout method and is already tried automatically first at optimization_level=3
transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3
)

print(transpiled)
