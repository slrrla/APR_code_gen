# The user only had a bare backend name, not a runnable program.
# This is the minimal scaffolding matching what was scraped: just referencing
# the default qasm_simulator with no noise/coupling map configuration,
# so it behaves like an ideal simulator (QV effectively 2^n_qubits, unbounded).

from qiskit import Aer, QuantumCircuit, execute

backend = Aer.get_backend('qasm_simulator')

qc = QuantumCircuit(5, 5)
qc.h(range(5))
qc.measure(range(5), range(5))

result = execute(qc, backend, shots=1024).result()
print(result.get_counts())
