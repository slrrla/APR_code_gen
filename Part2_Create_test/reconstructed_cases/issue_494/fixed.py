from qiskit import QuantumCircuit
import numpy  # referenced in answer as analogous to classical math libraries (e.g. numpy.sin)

# CNOT used to encode XOR: |y>|x> -> |x xor y>|x>
q = 2
qc = QuantumCircuit(q)
qc.cx(0, 1)

# Toffoli (AND) + CNOT (XOR) building block for a half adder;
# there is no general library for encoding arbitrary mathematical
# expressions into quantum circuits, so these "tricks" remain the
# standard approach as explained in the answer.
qc2 = QuantumCircuit(3)
qc2.ccx(0, 1, 2)
qc2.cx(0, 1)
