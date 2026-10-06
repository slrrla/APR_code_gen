import ast
import operator
from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    # placeholder for the user's file-reading function
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

def parse_hamiltonian(expression):
    """Parse scalar arithmetic and Pauli tensor products without executing code."""
    paulis = {"I": I, "X": X, "Y": Y, "Z": Z}
    binary = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.BitXor: operator.xor,
    }
    unary = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def convert(node):
        if isinstance(node, ast.Name) and node.id in paulis:
            return paulis[node.id]
        if isinstance(node, ast.Constant) and type(node.value) in (int, float, complex):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary:
            return binary[type(node.op)](convert(node.left), convert(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary:
            return unary[type(node.op)](convert(node.operand))
        raise ValueError("Unsupported Hamiltonian expression")

    return convert(ast.parse(expression, mode="eval").body)


hamiltonian = parse_hamiltonian(hamiltonian_string)
print(type(hamiltonian))
