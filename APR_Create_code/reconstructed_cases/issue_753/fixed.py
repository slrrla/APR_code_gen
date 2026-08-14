from qiskit import *
from qiskit.tools.visualization import plot_histogram
from qiskit.circuit.library import PhaseOracle
from qiskit.algorithms import Grover, AmplificationProblem

oracle = PhaseOracle('((A & C) | (B & D)) & ~(C & D)')
problem = AmplificationProblem(oracle=oracle, is_good_state=oracle.evaluate_bitstring)
backend = Aer.get_backend('qasm_simulator')
grover = Grover(quantum_instance=backend)
result = grover.amplify(problem)

counts = result.circuit_results[0]
print(counts)

# Fix: Tweedledum (used internally by PhaseOracle) orders variables by the
# order they first appear in the expression: A, C, B, D. Qiskit's bitstrings
# are little-endian, so the bit order in the returned counts is the reverse
# of that appearance order, i.e. D, B, C, A. Aqua's LogicalExpressionOracle
# used to sort variables alphabetically instead, which is why the same
# expression gave differently-ordered results there.
print('Variable order used by PhaseOracle (appearance order):', oracle.variables)

for bitstring, freq in counts.items():
    assignment = dict(zip(reversed(oracle.variables), bitstring))
    print(assignment, freq)
