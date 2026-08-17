from qiskit.opflow import I, X, Y, Z

def read_hamiltonian_from_file():
    # placeholder for the user's file-reading function
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

hamiltonian = eval(hamiltonian_string)
print(type(hamiltonian))
