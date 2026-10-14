from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo
# FIX: CSPLayout is not a registered layout_method -> import the explicit pass and its runner, because CSP layout must be invoked as a transpiler pass.
from qiskit.transpiler import CouplingMap, PassManager
from qiskit.transpiler.passes import CSPLayout

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# FIX: No CSP layout was computed -> run CSPLayout on the backend coupling map, because its result can be supplied as the initial layout.
layout_pass_manager = PassManager(CSPLayout(CouplingMap(backend.configuration().coupling_map)))
layout_pass_manager.run(qc)

transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    # FIX: 'csp_layout' is an invalid layout_method -> supply the computed initial_layout, because transpile accepts an explicit Layout.
    initial_layout=layout_pass_manager.property_set['layout']
)

print(transpiled)
