from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

# Build a circuit that already has some measurements on it
circuit = QuantumCircuit(3, 3)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure(0, 0)
circuit.measure(1, 1)

# Convert to a DAG so we can inspect and remove existing measurement nodes
my_dag = circuit_to_dag(circuit)

# Find all measurement operation nodes
measurement_nodes = my_dag.named_nodes('measure')

# Remove each measurement node rather than modifying it in place
for a_measurement_node in measurement_nodes:
    my_dag.remove_op_node(a_measurement_node)

# Convert back to a QuantumCircuit
circuit = dag_to_circuit(my_dag)

# Now add the extra gates and measure all qubits
circuit.cx(1, 2)
circuit.measure_all()

print(circuit)
