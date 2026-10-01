from qiskit import QuantumCircuit, transpile
# FIX: missing pass-manager imports -> import CSPLayout and ApplyLayout, because CSPLayout is not a valid transpile layout_method
from qiskit.transpiler import CouplingMap, PassManager
from qiskit.transpiler.passes import ApplyLayout, CSPLayout
from qiskit.providers.fake_provider import FakeVigo

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# FIX: invalid layout_method='csp_layout' -> explicitly run CSPLayout, because CSPLayout must be used through a pass manager
pass_manager = PassManager([
    CSPLayout(CouplingMap(backend.configuration().coupling_map)),
    ApplyLayout()
])
transpiled = pass_manager.run(qc)

print(transpiled)
