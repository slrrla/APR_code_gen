from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
# FIX: node.type no longer exists on DAG nodes -> import DAGOpNode for type checking, because modern Qiskit distinguishes op nodes by class
from qiskit.dagcircuit import DAGOpNode

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

dag = circuit_to_dag(circ)

counts = {}
# FIX: iterated dag.longest_path() -> iterate dag.op_nodes(), because the longest path only contains gates on the critical path, not all gates
for node in dag.op_nodes():
    # FIX: node.type == "op" -> isinstance(node, DAGOpNode), because DAG nodes no longer have a .type attribute
    if isinstance(node, DAGOpNode):
        counts[node.name] = counts.get(node.name, 0) + 1

print(counts)
