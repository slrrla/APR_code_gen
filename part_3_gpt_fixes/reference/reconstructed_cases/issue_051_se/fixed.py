from qiskit import QuantumCircuit, Aer, execute

def oracle():
    qc = QuantumCircuit(2, name='oracle')
    # CZ alone only flips the phase of |11>, since Z has no effect
    # on |0>; no extra gates are needed to mark |10>.
    qc.cz(0, 1)
    return qc

def diffuser():
    qc = QuantumCircuit(2, name='diffuser')
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    return qc

qc = QuantumCircuit(2, 2)
qc.h([0, 1])
qc.append(oracle().to_gate(), [0, 1])
qc.append(diffuser().to_gate(), [0, 1])
qc.measure([0, 1], [0, 1])

backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
print(result.get_counts())
