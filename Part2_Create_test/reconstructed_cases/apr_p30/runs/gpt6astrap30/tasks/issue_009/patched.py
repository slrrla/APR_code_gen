from itertools import permutations

from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo
from qiskit.transpiler.exceptions import TranspilerError

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = FakeVigo()

# csp_layout is not a layout plugin. Solve CSPLayout's default constraints
# directly, without its optional python-constraint dependency: all placements
# differ, and each two-qubit interaction uses adjacent physical qubits.
def csp_layout(circuit, backend):
    config = backend.configuration()
    edges = {tuple(edge) for edge in config.coupling_map}
    edges |= {(b, a) for a, b in edges}  # strict_direction=False
    interactions = [
        tuple(circuit.find_bit(q).index for q in instruction.qubits)
        for instruction in circuit.data
        if len(instruction.qubits) == 2
    ]
    # Exhaustive finite-domain search is sufficient for this 3-on-5 problem.
    for placement in permutations(range(config.n_qubits), circuit.num_qubits):
        if all((placement[a], placement[b]) in edges for a, b in interactions):
            return list(placement)
    raise TranspilerError('No layout satisfies the connectivity constraints')


transpiled = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    initial_layout=csp_layout(qc, backend)
)

print(transpiled)
