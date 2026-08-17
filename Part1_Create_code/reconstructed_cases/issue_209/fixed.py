from qiskit import transpile
from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit.test.mock import FakeVigo

# Use a local fake device that mimics the real backend's properties
fake_vigo = FakeVigo()
server = fake_vigo

# Run Shor's algorithm to factor N=15
shor = Shor(N=15)
result = shor.run(QuantumInstance(server))

shor_compiled = transpile(result['circuit'], backend=server, optimization_level=3)
print('gates = ', shor_compiled.count_ops())
print('depth = ', shor_compiled.depth())
