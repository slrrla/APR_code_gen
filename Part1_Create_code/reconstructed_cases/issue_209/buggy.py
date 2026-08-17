from qiskit import IBMQ, transpile
from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance

# Connect to the real IBMQ paying device (requires credentials/access)
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
server = provider.get_backend('ibmq_16_melbourne')

# Run Shor's algorithm to factor N=15
shor = Shor(N=15)
result = shor.run(QuantumInstance(server))

shor_compiled = transpile(result['circuit'], backend=server, optimization_level=3)
print('gates = ', shor_compiled.count_ops())
print('depth = ', shor_compiled.depth())
