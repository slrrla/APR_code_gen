from qiskit import BasicAer
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import PhaseOracle

log_expr = '((A & B) | (B & C)) & ~ (B & D)'
algorithm = Grover(PhaseOracle(log_expr))
backend = BasicAer.get_backend('qasm_simulator')
result = algorithm.run(backend)
