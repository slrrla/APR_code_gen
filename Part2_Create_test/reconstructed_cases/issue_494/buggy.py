from qiskit import QuantumCircuit

# CNOT used to encode XOR: |y>|x> -> |x xor y>|x>
q = 2
qc = QuantumCircuit(q)
qc.cx(0, 1)

# Attempt to build part of a half adder using Toffoli (AND) + CNOT (XOR)
qc2 = QuantumCircuit(3)
qc2.ccx(0, 1, 2)
qc2.cx(0, 1)
