from qiskit.qasm3 import dumps
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit import transpile, assemble, qasm3
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.quantum_info import Statevector

# Step 1: Define parameters
theta = Parameter('theta')
phi = Parameter('phi')

# Create a quantum circuit with 2 qubits
qc = QuantumCircuit(2)

# Add parameterized gates
qc.rx(theta, 0)
qc.ry(phi, 1)
qc.cx(0, 1)

# Draw the original circuit
qc.draw('mpl')

# Step 2: Generate QASM 3 code
qasm_str = dumps(qc)
print("Generated QASM 3 code:")
print(qasm_str)

dag = circuit_to_dag(qasm3.loads(qasm_str))
recreated_circuit = dag_to_circuit(dag)
recreated_circuit.draw()

# FIX: use the Parameter instances that actually live in recreated_circuit,
# matched by name, instead of the original theta/phi objects
parameter_values = {}
for param in recreated_circuit.parameters:
    parameter_values[param] = 1.57 if param.name == 'theta' else 3.14

bound_circuit = recreated_circuit.assign_parameters(parameter_values, inplace=False)
