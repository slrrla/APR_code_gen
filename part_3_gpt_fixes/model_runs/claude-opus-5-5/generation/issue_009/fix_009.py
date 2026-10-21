from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo
# FIX: no CSP layout_method exists -> import CSPLayout pass tooling, because CSP must be run as a pass to force its use
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes import CSPLayout

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# FIX: compute the layout with CSPLayout explicitly -> run pass to get layout, because transpile has no 'csp_layout' method
pm = PassManager(CSPLayout(CouplingMap(backend.configuration().coupling_map)))
pm.run(qc)
csp_layout = pm.property_set['layout']

transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    # FIX: invalid layout_method='csp_layout' -> initial_layout=csp_layout, because only trivial/dense/noise_adaptive/sabre are valid methods
    initial_layout=csp_layout
)

print(transpiled)
