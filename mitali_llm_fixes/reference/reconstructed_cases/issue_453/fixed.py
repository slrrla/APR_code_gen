from typing import Sequence, Union
from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit, AncillaQubit
from qiskit.circuit.instruction import Instruction
from qiskit.circuit.quantumcircuit import QubitSpecifier, ClbitSpecifier


def compose_with_auto_ancillas(
    self,
    other: Union["QuantumCircuit", Instruction],
    qubits=None,
    clbits=None,
    front: bool = False,
    inplace: bool = False,
    wrap: bool = False,
):
    num_self_ancillas = len(self.ancillas)
    num_other_ancillas = len(other.ancillas)
    if num_other_ancillas > 0:
        if num_self_ancillas < num_other_ancillas:
            extra_ancillas = []
            for _ in range(num_other_ancillas - num_self_ancillas):
                extra_ancillas.append(AncillaQubit())
            self.add_bits(extra_ancillas)
        qubits = qubits + self.ancillas[0:num_other_ancillas]
    return self.compose(other, qubits, clbits, front, inplace, wrap)


QuantumCircuit.compose_with_auto_ancillas = compose_with_auto_ancillas

# A subcircuit with its own ancilla qubits:
qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

# The main circuit:
# Note that, you don't have to add any ancilla at the beginning,
# they will be added when needed.
circ = QuantumCircuit(4)
circ.h([0, 1, 2, 3])
circ.barrier()
circ.compose_with_auto_ancillas(qc1, [0, 1, 2, 3], inplace=True)
