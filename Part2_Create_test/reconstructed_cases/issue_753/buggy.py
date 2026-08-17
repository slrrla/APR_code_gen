from qiskit import *
from qiskit.tools.visualization import plot_histogram
from qiskit.circuit.library import PhaseOracle
from qiskit.algorithms import Grover, AmplificationProblem

oracle = PhaseOracle('((A & C) | (B & D)) & ~(C & D)')
problem = AmplificationProblem(oracle=oracle, is_good_state=oracle.evaluate_bitstring)
backend = Aer.get_backend('qasm_simulator')
grover = Grover(quantum_instance=backend)
result = grover.amplify(problem)

# Bug: user assumes the returned bitstring maps to variables in
# alphabetical order (A, B, C, D) when printing/interpreting the counts.
print(result.circuit_results[0])
