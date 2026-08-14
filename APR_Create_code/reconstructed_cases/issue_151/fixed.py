import time
from qiskit import execute, BasicAer
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle

backend = BasicAer.get_backend('qasm_simulator')

def build_circuit(n):
    # n is input size associated with oracle,
    # and some other components are omitted.
    oracle = LogicalExpressionOracle('a & b')
    grover = Grover(oracle)
    circuit = grover.construct_circuit()
    return circuit

start = time.time()
circuits = [build_circuit(n) for n in range(0, 10)]
result = execute(circuits, backend=backend).result()
end = time.time()
