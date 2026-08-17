from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag

circ = QuantumCircuit(4, 4)
circ.h(0)
circ.h(1)
circ.h(2)
circ.h(3)
circ.cx(0, 1)
circ.cx(1, 2)
circ.cx(2, 3)
circ.rz(0.5, 0)
circ.measure(0, 0)
circ.measure(1, 1)
circ.measure(2, 2)
circ.measure(3, 3)

# Counting gates only along the longest path of the DAG
dag = circuit_to_dag(circ)

counts = {}
for node in dag.longest_path():
    if node.type == "op":
        counts[node.name] = counts.get(node.name, 0) + 1

print(counts)
