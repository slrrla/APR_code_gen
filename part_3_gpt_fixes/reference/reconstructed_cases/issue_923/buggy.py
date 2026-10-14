# Attempt to build an Ising Hamiltonian using only WeightedPauliOperator,
# without constructing the problem via docplex/QuadraticProgram first.
from qiskit.aqua.operators import WeightedPauliOperator

# specify problem
n = 3
a = 1.0
k = 2
t = range(1, n+1)

# No actual construction of the Hamiltonian from the problem is done;
# the user does not know how to translate the objective into Pauli terms.
H = WeightedPauliOperator(paulis=[])

print('Ising Hamiltonian:')
print(H.print_details())
