from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

circ1 = QuantumCircuit(3, 3)
circ1.h([0, 1, 2])

# Remove classical bits from circ1 before composing it into a larger circuit
dag = circuit_to_dag(circ1)
dag.remove_clbits(*circ1.clbits)
circ1 = dag_to_circuit(dag)

circ2 = QuantumCircuit(3)
circ2.x([0, 1, 2])

circ = QuantumCircuit(6)
circ.compose(circ1, [0, 1, 2], inplace=True)
circ.compose(circ2, [3, 4, 5], inplace=True)

print(circ)
