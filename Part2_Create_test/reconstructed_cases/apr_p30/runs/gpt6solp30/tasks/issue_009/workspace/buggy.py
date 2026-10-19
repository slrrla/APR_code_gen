from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# Let the level-3 preset pass manager choose a supported layout strategy (VF2, then Sabre).
transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
)

print(transpiled)
