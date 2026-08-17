# Fix was environment-level, not a code change:
#   pip install --ignore-installed qiskit-terra qiskit-aer
# This reinstalls qiskit-terra/qiskit-aer against the currently installed
# numpy, resolving the ABI ("size changed") mismatch. The imports below
# then succeed with no code modification needed.
from qiskit import QuantumCircuit, Aer, BasicAer, execute
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = BasicAer.get_backend('qasm_simulator')
result = execute(qc, backend).result()
counts = result.get_counts()
print(counts)
