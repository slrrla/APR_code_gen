from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# FIX: PauliOp(hamiltonian_string) raised TypeError -> eval(hamiltonian_string), because PauliOp only accepts Pauli objects, while eval runs the string as opflow code using the imported I, X, Y, Z operators.
hamiltonian = eval(hamiltonian_string)
print(type(hamiltonian))
