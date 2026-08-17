from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.passes import RemoveResetInZeroState
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import GroverOperator

# Build a state preparation circuit using QuantumCircuit.initialize
init = QuantumCircuit(3)
init.initialize([1, 0, 0, 0, 0, 0, 0, 0], init.qubits)

# Decompose the Initialize instruction and strip the resets so the
# resulting circuit is unitary and can be used as state_preparation.
stateprep = RemoveResetInZeroState()(init.decompose())

state_preparation = stateprep

# Some oracle for demonstration purposes
oracle = QuantumCircuit(3)
oracle.z(2)

problem = AmplificationProblem(oracle, state_preparation=state_preparation)

grover = Grover()
result = grover.amplify(problem)
print(result.top_measurement)
