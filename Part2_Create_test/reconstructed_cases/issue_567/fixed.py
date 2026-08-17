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

# Fixed approach: use dag.multigraph_layers(), which captures the true
# topological dependencies between gates, so only the gates that truly
# belong to the last n layers get removed.
dag = circuit_to_dag(qc)
layers = list(dag.multigraph_layers())
n_remove = 2
# the extra minus 1 since the last layer consists of output nodes (qubits and clbits).
for layer in layers[-n_remove - 1:]:
    for node in layer:
        if node.type == 'op':
            dag.remove_op_node(node)
new_qc = dag_to_circuit(dag)
print(new_qc)
