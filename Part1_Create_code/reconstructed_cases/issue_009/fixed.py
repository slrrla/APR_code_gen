from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# CSPLayout is tried automatically at optimization_level>=2/3.
# To pick a specific fallback layout method, use a valid name such as
# 'trivial', 'dense', 'noise_adaptive', or 'sabre'.
transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    layout_method='noise_adaptive'
)

print(transpiled)
