# Minimal reproduction of the reported Grover's algorithm behavior
# using an IntegerComparator-based oracle for the query "array[i] < n"
# on the array [7,6,5,4,3,2,1,0] (encoded as indices 0..7 in binary).
#
# BUG: the number of Grover iterations is computed assuming the number
# of solutions M is always much smaller than the search space size N,
# using the standard optimal_num_iterations formula with a fixed M=1.
# This ignores the fact that for n=5,6,7 the true number of solutions
# M is greater than N/2, which causes Grover's algorithm to amplify the
# WRONG group of states (the non-solutions) instead of the solutions.

from qiskit import QuantumCircuit
from qiskit.circuit.library import IntegerComparator
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.utils import QuantumInstance
from qiskit import Aer

def less_than_oracle(n, num_qubits):
    # marks all states whose integer value is < n
    comp = IntegerComparator(num_qubits, n, geq=False)
    qc = QuantumCircuit(comp.num_qubits)
    qc.append(comp, range(comp.num_qubits))
    return qc

def is_good_state(bitstring, n, num_qubits):
    value = int(bitstring[-num_qubits:], 2)
    return value < n

num_qubits = 3
N = 2 ** num_qubits
n = 5  # query: find elements < 5 in [7,6,5,4,3,2,1,0]

oracle = less_than_oracle(n, num_qubits)
problem = AmplificationProblem(
    oracle,
    is_good_state=lambda bitstring: is_good_state(bitstring, n, num_qubits)
)

# BUG: assumes M = 1 regardless of the actual number of solutions
num_iterations = Grover.optimal_num_iterations(1, N)

quantum_instance = QuantumInstance(Aer.get_backend('qasm_simulator'), shots=1024)
grover = Grover(iterations=num_iterations, quantum_instance=quantum_instance)
result = grover.amplify(problem)

print("n =", n)
print("iterations used:", num_iterations)
print("top measurement:", result.top_measurement)
