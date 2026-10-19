# BASED ON: https://qiskit.org/textbook/ch-applications/hhl_tutorial.html#4.-Qiskit-Implementation
# Importing standard Qiskit libraries and configuring account
from qiskit import Aer
from qiskit.circuit.library import QFT
from qiskit.aqua.components.eigs import EigsQPE
from qiskit.aqua.components.reciprocals import LookupRotation
from qiskit.aqua.operators import MatrixOperator
from qiskit.aqua.components.initial_states import Custom
import numpy as np

# Linear equations solvers
from qiskit.aqua.algorithms import HHL, NumPyLSsolver  # HHL - quantum, NumPyLSolver - classical


def create_eigs(matrix, num_ancillae, num_time_slices, negative_evals):
    ne_qfts = [None, None]
    if negative_evals:
        num_ancillae += 1
        ne_qfts = [QFT(num_ancillae - 1), QFT(num_ancillae - 1).inverse()]

    # Construct the eigenvalues estimation using the PhaseEstimationCircuit
    return EigsQPE(MatrixOperator(matrix=matrix),
                   QFT(num_ancillae).inverse(),
                   num_time_slices=num_time_slices,
                   num_ancillae=num_ancillae,
                   expansion_mode='suzuki',
                   expansion_order=2,
                   evo_time=None,
                   negative_evals=negative_evals,
                   ne_qfts=ne_qfts)


def HHLsolver(matrix, vector, backend, no_ancillas, no_time_slices):
    orig_size = len(vector_b)
    # adapt the matrix to have dimension 2^k
    matrix, vector, truncate_powerdim, truncate_hermitian = HHL.matrix_resize(matrix_A, vector_b)

    # find eigenvalues of the matrix with phase estimation (i.e. calc. exponential of A, apply
    # phase estimation) to get exp(lambda) and then inverse QFT to get lambdas themselves
    eigs = create_eigs(matrix, no_ancillas, no_time_slices, False)

    # num_q - Number of qubits required for the matrix Operator instance
    # num_a - Number of ancillary qubits for Eigenvalues instance
    num_q, num_a = eigs.get_register_sizes()

    # construct circuit for finding reciprocals of eigenvalues
    reci = LookupRotation(negative_evals=eigs._negative_evals, evo_time=eigs._evo_time)

    # preparing init state for HHL, i.e. the state containing vector b
    init_state = Custom(num_q, state_vector=vector)

    # construct circuit for HHL based on matrix A, vector B and reciprocals of eigenvalues
    algo = HHL(matrix, vector, truncate_powerdim, truncate_hermitian, eigs, init_state, reci, num_q, num_a, orig_size)

    # solution on quantum computer
    result = algo.run(quantum_instance=backend)
    print("Solution:\t\t", np.round(result['solution'], 5))
    print("Probability:\t\t %f" % result['probability_result'])

    # reference solution - NumPyLSsolver = Numpy LinearSystem algorithm (classical).
    result_ref = NumPyLSsolver(matrix, vector).run()
    print("Classical Solution:\t", np.round(result_ref['solution'], 5))


matrix_A = np.array([[1.5, 0.5], [0.5, 1.5]])
vector_b = [0.9010, -0.4339]
# x = A^(-1)b = [0.78420, -0.55066] #expected result

processor = Aer.get_backend('statevector_simulator')
no_ancillas = 3  # number of ancilla qubits
no_time_slices = 50  # number of timeslices in exponential of matrix A (exp(i*A*t))

HHLsolver(matrix_A, vector_b, processor, no_ancillas, no_time_slices)
