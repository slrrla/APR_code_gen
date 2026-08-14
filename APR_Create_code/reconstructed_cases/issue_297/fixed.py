from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit import transpile

N_COUNT = 8  # number of counting qubits

def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2, 7, 8, 11, 13]:
        raise ValueError("'a' must be 2,7,8,11 or 13")
    U = QuantumCircuit(4)
    for iteration in range(power):
        if a in [2, 13]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a == 11:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U

def qpe_amod15(a):
    qc = QuantumCircuit(4 + N_COUNT, N_COUNT)
    for q in range(N_COUNT):
        qc.h(q)
    qc.x(N_COUNT)
    for q in range(N_COUNT):
        qc.append(c_amod15(a, 2**q), [q] + [i + N_COUNT for i in range(4)])
    qc.append(QFT(N_COUNT, inverse=True), range(N_COUNT))
    qc.measure(range(N_COUNT), range(N_COUNT))
    return qc

# 'a' must be one of the valid values: [2, 7, 8, 11, 13]
a = 7

qc = qpe_amod15(a)
sim = AerSimulator()
tqc = transpile(qc, sim)
result = sim.run(tqc, shots=1).result()
counts = result.get_counts()
print(counts)
