from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# Use a supported layout plugin; CSPLayout is a separate analysis pass.
transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    layout_method='sabre'
)

print(transpiled)
