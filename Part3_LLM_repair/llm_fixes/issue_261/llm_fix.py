from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# FIX: PauliOp cannot construct an operator from a string -> evaluate the saved expression, because the expression uses imported Qiskit operators
hamiltonian = eval(hamiltonian_string)
print(type(hamiltonian))

