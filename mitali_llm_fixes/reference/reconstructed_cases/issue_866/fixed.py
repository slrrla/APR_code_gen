# Fix: Grover's algorithm assumes M << N. When the true number of
# solutions M exceeds N/2, the oracle marking "< n" differs from the
# oracle marking ">= n" only by an unobservable global phase, so
# Grover amplifies the complementary (larger) set instead. The fix is
# to compute the actual number of solutions M, and if M > N/2, search
# for the complement query instead (">= n") and invert the
# interpretation of the result, using the correct number of
# iterations for that smaller problem.

from qiskit import QuantumCircuit
from qiskit.circuit.library import IntegerComparator
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.utils import QuantumInstance
from qiskit import Aer

def less_than_oracle(n, num_qubits):
    comp = IntegerComparator(num_qubits, n, geq=False)
    qc = QuantumCircuit(comp.num_qubits)
    qc.append(comp, range(comp.num_qubits))
    return qc

def geq_oracle(n, num_qubits):
    comp = IntegerComparator(num_qubits, n, geq=True)
    qc = QuantumCircuit(comp.num_qubits)
    qc.append(comp, range(comp.num_qubits))
    return qc

def is_good_state(bitstring, n, num_qubits, geq=False):
    value = int(bitstring[-num_qubits:], 2)
    return value >= n if geq else value < n

num_qubits = 3
N = 2 ** num_qubits
n = 5  # query: find elements < 5 in [7,6,5,4,3,2,1,0]

# actual number of solutions for "< n"
M = n
use_complement = M > N / 2

if use_complement:
    oracle = geq_oracle(n, num_qubits)
    M_search = N - M
    good_state = lambda bitstring: is_good_state(bitstring, n, num_qubits, geq=True)
else:
    oracle = less_than_oracle(n, num_qubits)
    M_search = M
    good_state = lambda bitstring: is_good_state(bitstring, n, num_qubits, geq=False)

problem = AmplificationProblem(oracle, is_good_state=good_state)

# use the correct number of solutions for the (smaller) problem actually searched
num_iterations = Grover.optimal_num_iterations(M_search, N)

quantum_instance = QuantumInstance(Aer.get_backend('qasm_simulator'), shots=1024)
grover = Grover(iterations=num_iterations, quantum_instance=quantum_instance)
result = grover.amplify(problem)

top = result.top_measurement
if use_complement:
    value = int(top, 2)
    # complement search found a ">= n" state; the actual "< n" solutions
    # are simply all other values, report accordingly
    print("n =", n, "(searched complement '>= n' due to M > N/2)")
else:
    print("n =", n)

print("iterations used:", num_iterations)
print("top measurement:", top)
