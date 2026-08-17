import numpy as np
from math import ceil, log2
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.extensions import Initialize

bitstring = ("ATGGTGCTGTCTGCGGCTGACAAGACCAACGTCAAGGGTGTCTTCTCCAAAATCGGTGGC"
             "CATGCTGAGGAGTATGGCGCCGAGACCCTGGAGAGGATGTTCATCGCCTACCCCCAGACC"
             "AAGACCTACTTCCCCCACTTTGACCTGCAGCACGGCTCTGCTCAGATCAAGGCCCATGGC"
             "AAGAAGGTGGCGGCTGCCCTAGTTGAAGCTGTCAACCACATCGATGACATTGCGGGTGCT"
             "CTCTCCAAGCTCAGTGACCTCCACGCCCAAAAGCTCCGTGTGGACCCTGTCAACTTCAAA"
             "TTCCTGGGCCACTGCTTCCTGGTGGTGGTTGCCATCCACCACCCCGCTGCCCTGACCCCA"
             "GAGGTCCACGCTTCCCTGGACAAGTTCATGTGCGCCGTGGGTGCTGTGCTGACTGCCAAG"
             "TACCGTTAG")

bitstring = bitstring.ljust(512, 'A')
bitstring_len = len(bitstring)

bitstring = bitstring.replace("A", "00")
bitstring = bitstring.replace("C", "01")
bitstring = bitstring.replace("G", "10")
bitstring = bitstring.replace("T", "11")

n = ceil(log2(len(bitstring))) + 1
amplitude = np.sqrt(1.0 / 2**(n - 1))

desired_vector = np.array(list(bitstring))
desired_vector = [int(x) for x in desired_vector]
# FIX: properly normalize by dividing by the actual vector norm
norm = np.linalg.norm(desired_vector)
desired_vector = desired_vector / norm

qr = QuantumRegister(n)
cr = ClassicalRegister(n)
qc = QuantumCircuit(qr, cr)
qc_init = QuantumCircuit(n)
inverse_qc_init = QuantumCircuit(n)

qc_init.initialize(desired_vector, range(n))
