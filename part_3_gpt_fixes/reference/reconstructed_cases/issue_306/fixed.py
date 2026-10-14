from qiskit import BasicAer
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import PhaseOracle

log_expr = '((A & B) | (B & C)) & ~ (B & D)'
problem = AmplificationProblem(PhaseOracle(log_expr))
backend = BasicAer.get_backend('qasm_simulator')
grover = Grover(quantum_instance=backend)
result = grover.amplify(problem)
