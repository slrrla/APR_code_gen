# Fails with:
# ValueError: numpy.ndarray size changed, may indicate binary incompatibility.
# Expected 88 from C header, got 80 from PyObject
# This is caused by a numpy/qiskit-aer binary mismatch in the environment.
from qiskit import QuantumCircuit, Aer, BasicAer, execute
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = BasicAer.get_backend('qasm_simulator')
result = execute(qc, backend).result()
counts = result.get_counts()
print(counts)
