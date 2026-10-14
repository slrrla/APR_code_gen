# FIX: SparsePauliOp cannot be initialized from a dense matrix -> import Operator to wrap the matrix, because from_operator converts it to a Pauli representation
from qiskit.quantum_info import SparsePauliOp, Operator

Hamiltonian = [
    [ 4.07981221, -3.6713615 , 1.3943662 , -1.05164319],
    [-3.6713615 , 5.88262911, -4.14084507, 1.37558685],
    [ 1.3943662 , -4.14084507, 5.83098592, -3.54929577],
    [-1.05164319, 1.37558685, -3.54929577, 3.79812207]
]

# FIX: the dense matrix was passed as Pauli input data -> convert from an Operator, because the matrix must first be interpreted as an operator
H_op = SparsePauliOp.from_operator(Operator(Hamiltonian)).to_operator()
print(H_op)
