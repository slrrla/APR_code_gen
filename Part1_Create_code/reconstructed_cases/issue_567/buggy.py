from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

qc = QuantumCircuit(2)
qc.sdg(0)
qc.h(0)
qc.y(1)
qc.h(1)
qc.s(1)
qc.cx(0, 1)
qc.cx(1, 0)
qc.h(0)
qc.s(0)
qc.h(0)
qc.h(1)
qc.s(1)
qc.h(1)
print(qc)

# Previous (buggy) approach: remove the last n "layers" using dag.layers(),
# which greedily assigns nodes to layers and does not respect the true
# topological dependency structure of the circuit. This can remove more
# gates than intended (e.g. an extra Hadamard on qubit 1 that should have
# been kept).
dag = circuit_to_dag(qc)
layers = list(dag.layers())
n_remove = 2
for layer in layers[-n_remove:]:
    for node in layer['graph'].op_nodes():
        dag.remove_op_node(node)
new_qc = dag_to_circuit(dag)
print(new_qc)
