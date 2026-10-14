# Fixed: understanding what each optimization_level actually does under
# the hood (per preset pass managers source code), and confirming that
# higher levels apply more passes (e.g. commutative cancellation,
# unitary synthesis) that do simplify circuits when applicable.

from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import Aer

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(0)

backend = Aer.get_backend('qasm_simulator')

for level in [0, 1, 2, 3]:
    transpiled = transpile(qc, backend=backend, optimization_level=level)
    print(f"optimization_level={level}")
    print(transpiled)

# Level 1 optimization passes (from qiskit source):
# _opt = [
#     Optimize1qGatesDecomposition(basis_gates),
#     CommutativeCancellation(basis_gates=basis_gates),
# ]

# Level 3 optimization passes (from qiskit source):
# _opt = [
#     Collect2qBlocks(),
#     ConsolidateBlocks(basis_gates=basis_gates, target=target),
#     UnitarySynthesis(
#         basis_gates,
#         approximation_degree=approximation_degree,
#         coupling_map=coupling_map,
#         backend_props=backend_properties,
#         method=unitary_synthesis_method,
#         plugin_config=unitary_synthesis_plugin_config,
#         target=target,
#     ),
#     Optimize1qGatesDecomposition(basis_gates),
#     CommutativeCancellation(),
# ]
