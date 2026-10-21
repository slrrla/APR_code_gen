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
    optimization_level=3
    # FIX: layout_method='csp_layout' is not a valid public layout method -> removed the argument, because level 3 already runs the CSP layout search first when the backend has a coupling map
)

print(transpiled)
