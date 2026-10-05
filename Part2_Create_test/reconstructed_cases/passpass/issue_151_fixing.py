import time
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle

backend = AerSimulator()

def build_circuit(n):
    oracle = LogicalExpressionOracle('a & b')
    grover = Grover(oracle)
    circuit = grover.construct_circuit()
    return circuit

start = time.time()
circuits = [build_circuit(n) for n in range(0, 10)]
transpiled = transpile(circuits, backend=backend)
result = backend.run(transpiled).result()
end = time.time()
print(result.get_counts())
