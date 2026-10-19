import time
from qiskit import BasicAer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle

backend = BasicAer.get_backend('qasm_simulator')

def quantum(n):
    # n is input size associated with oracle,
    # and some other components are omitted.
    oracle = LogicalExpressionOracle('a & b')
    result = Grover(oracle).run(QuantumInstance(backend))
    return result

for n in range(0, 10):
    start = time.time()
    quantum(n)
    end = time.time()
