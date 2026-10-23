from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    # FIX: invalid layout_method='csp_layout' -> removed the argument, because CSP is not a valid layout_method and optimization_level=3 already tries the perfect-layout search (CSPLayout/VF2Layout) first
)

print(transpiled)
