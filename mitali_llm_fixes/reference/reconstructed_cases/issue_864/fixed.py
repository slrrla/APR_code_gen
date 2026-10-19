from qiskit import *
from qiskit.quantum_info import Operator

qr = QuantumRegister(3, 'q')
cr = ClassicalRegister(0, 'c')
circuit = QuantumCircuit(qr, cr)
circuit.cz(qr[0], qr[1])
circuit.cz(qr[0], qr[2])

simulator = Aer.get_backend('unitary_simulator')
result = execute(circuit, backend=simulator).result()

def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:" + fmt + "}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end=" ")
        print("")

matprint(result.get_unitary().data)

# Reverse qubit ordering to match Braket's big-endian convention
print(Operator(circuit).reverse_qargs().to_matrix())
