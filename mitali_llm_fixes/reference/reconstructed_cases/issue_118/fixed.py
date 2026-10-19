# To use a classical function as a quantum oracle, you (the implementer)
# must construct a reversible circuit U_f that implements the function's
# input/output behaviour explicitly, e.g. following Simon's algorithm
# tutorial: build the oracle from a secret bitstring c.

from qiskit import QuantumCircuit

def simon_oracle(c):
    """Build a reversible oracle circuit for Simon's algorithm from a
    secret string c, satisfying f(x) = f(y) iff y = x xor c."""
    n = len(c)
    qc = QuantumCircuit(2 * n)
    # copy x onto the second register (identity part of f)
    for i in range(n):
        qc.cx(i, n + i)
    # if c is not all zeros, apply the periodicity according to c
    if '1' in c:
        i = c.find('1')
        for j in range(n):
            if c[j] == '1':
                qc.cx(i, n + j)
    return qc

c = '101'
n = len(c)

qc = QuantumCircuit(2 * n, n)
qc.h(range(n))
qc.append(simon_oracle(c), range(2 * n))
qc.h(range(n))
qc.measure(range(n), range(n))

print(qc)
