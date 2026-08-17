from qiskit import QuantumCircuit

# circ1 has classical registers, which causes trouble when composing
# into a bigger circuit that doesn't have matching classical registers
circ1 = QuantumCircuit(3, 3)
circ1.h([0, 1, 2])

circ2 = QuantumCircuit(3)
circ2.x([0, 1, 2])

circ = QuantumCircuit(6)
# This will raise an error because circ1 carries classical bits
# that circ does not have registers for
circ.compose(circ1, [0, 1, 2], inplace=True)
circ.compose(circ2, [3, 4, 5], inplace=True)

print(circ)
