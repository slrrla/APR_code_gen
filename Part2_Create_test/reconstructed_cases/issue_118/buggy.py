# The asker has only a classical Python function acting as a "blackbox".
# It cannot directly be used as a quantum oracle because it is not
# expressed as a reversible unitary circuit U_f.

def func(input):
    return not input

# Attempt to use this classical function directly in a quantum circuit.
from qiskit import QuantumCircuit

n = 1
qc = QuantumCircuit(n + 1, n)
qc.h(range(n))

# BUG: there is no way to "plug in" a plain classical function like this
# into a QuantumCircuit -- func() is not a reversible gate/oracle.
qc.append(func, range(n + 1))  # this is not valid / not how oracles work

qc.h(range(n))
qc.measure(range(n), range(n))

print(qc)
