import qiskit

def create_circuit():
    qr3 = qiskit.QuantumRegister(2)
    cr3 = qiskit.ClassicalRegister(2)
    qc3 = qiskit.QuantumCircuit(qr3, cr3)
    qc3.h(qr3[0])              # H
    qc3.cx(qr3[0], qr3[1])     # CNOT
    return qc3

if __name__ == "__main__":
    qc = create_circuit()
    print(qc)
