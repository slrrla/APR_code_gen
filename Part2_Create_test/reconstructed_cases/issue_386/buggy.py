from openfermion.ops import QubitOperator

# The user is trying to construct a Hamiltonian using the ProjectQ/OpenFermion
# style QubitOperator, but wants to do this with qiskit instead.
h = 5.9*QubitOperator('') + 0.21*QubitOperator('Z0') - 6.12*QubitOperator('Z1') - 2.14*(QubitOperator('X0 X1')+QubitOperator('Y0 Y1')) + 9.6*(QubitOperator('')-QubitOperator('Z2')) - 3.9*(QubitOperator('X1 X2') + QubitOperator('Y1 Y2'))

print(h)
