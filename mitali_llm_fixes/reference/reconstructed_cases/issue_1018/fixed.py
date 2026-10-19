import qiskit

def TestA():
    qr = qiskit.QuantumRegister(5, name="reg1")
    cr = qiskit.ClassicalRegister(4, name="classic_reg")
    qc = qiskit.QuantumCircuit(qr, cr)
    qc.h(0)
    qc.cx(0, 4)
    qc.h(1)
    qc.cz(1, 0)
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    print(qc)

TestA()
TestA()
