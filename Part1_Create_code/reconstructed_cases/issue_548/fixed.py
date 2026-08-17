from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

circ = QuantumCircuit(2, 2)
circ.x(1)
circ.h(0)
circ.h(1)
circ.cx(0, 1)
circ.h(0)
circ.measure(0, 0)
circ.measure(1, 1)

# Use DAGCircuit.layers() to properly decompose the circuit into layers
# of operations that can act in parallel.
dag = circuit_to_dag(circ)
for i, layer in enumerate(dag.layers()):
    layer_as_circuit = dag_to_circuit(layer['graph'])
    print(f"layer[{i}] =")
    print(layer_as_circuit)
