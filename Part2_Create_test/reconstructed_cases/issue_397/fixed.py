from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate

# Build a parameterized SparsePauliOp representing exp(-i(XZ*a + YZ*b))
a, b = Parameter('a'), Parameter('b')
op = SparsePauliOp(['XZ', 'YZ'], coeffs=[a, b])

# Use PauliEvolutionGate to build the exponential of the operator
evolution_gate = PauliEvolutionGate(op, time=1.0)

circuit = QuantumCircuit(op.num_qubits)
circuit.append(evolution_gate, range(op.num_qubits))

print(circuit)
