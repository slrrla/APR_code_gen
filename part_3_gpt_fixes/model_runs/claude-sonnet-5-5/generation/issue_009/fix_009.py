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
    # FIX: invalid layout_method 'csp_layout' -> use valid 'sabre', because CSPLayout is a pass, not a layout_method option, and at optimization_level=3 it is already tried first automatically
    layout_method='sabre'
)

print(transpiled)
