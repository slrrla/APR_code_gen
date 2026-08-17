import qiskit

def TestA():
    qr = qiskit.QuantumRegister(5)
    cr = qiskit.ClassicalRegister(4)
    qc = qiskit.QuantumCircuit(qr, cr)
    qc.h(0)
    qc.cx(0, 4)
    qc.h(1)
    qc.cz(1, 0)
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    print(qc)

TestA()
TestA()
