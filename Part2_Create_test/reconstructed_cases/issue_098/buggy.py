from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram

a = QuantumCircuit(1)
a.z(0)
a.x(0)
a.h(0)
a.sdg(0)
a.t(0)
backend = Aer.get_backend('qasm_simulator')
result = execute(a, backend).result()
counts = result.get_counts()
plot_histogram(counts)
