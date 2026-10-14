# Corrected understanding: transpilation does NOT require building the
# full 2^n x 2^n unitary. It operates on individual 1- and 2-qubit gates
# (or alternative representations like graphs/DAGs), not full matrices.

from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo

n = 5  # small n used only to keep this runnable; question concerns n > 100
qc = QuantumCircuit(n)
for i in range(n):
    qc.h(i)
for i in range(n - 1):
    qc.cx(i, i + 1)

backend = FakeVigo()
# Transpilation works on gate-level representations (basis gates, DAGs),
# never on the full exponential-size unitary matrix.
transpiled = transpile(qc, backend=backend, optimization_level=1)
print(transpiled.count_ops())
