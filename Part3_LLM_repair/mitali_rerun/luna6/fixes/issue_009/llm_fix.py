from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo
# FIX: `csp_layout` is not a valid `layout_method` -> import and run CSPLayout directly, because CSPLayout is a transpiler pass.
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes import CSPLayout

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# FIX: `transpile` cannot select CSPLayout via `layout_method` -> obtain its layout by running the pass, because CSPLayout is not a registered method.
layout_pass = PassManager([CSPLayout(CouplingMap(backend.configuration().coupling_map))])
layout_pass.run(qc)
initial_layout = layout_pass.property_set["layout"]

transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    # FIX: `csp_layout` is not a supported `layout_method` -> pass CSPLayout's result as the initial layout, because this applies its placement during transpilation.
    initial_layout=initial_layout
)

print(transpiled)
