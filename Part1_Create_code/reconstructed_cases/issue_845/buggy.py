from qiskit.circuit import QuantumCircuit
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import GroverOperator

# Build a state preparation circuit using QuantumCircuit.initialize
# This uses qiskit.extensions.initialize under the hood, which introduces
# a qubit reset (non-unitary), making it invalid to use directly as
# state_preparation for AmplificationProblem.
init = QuantumCircuit(3)
init.initialize([1, 0, 0, 0, 0, 0, 0, 0], init.qubits)

state_preparation = init

# Some oracle for demonstration purposes
oracle = QuantumCircuit(3)
oracle.z(2)

problem = AmplificationProblem(oracle, state_preparation=state_preparation)

grover = Grover()
result = grover.amplify(problem)
print(result.top_measurement)
