import qiskit

def create_circuit():
    qr3 = qiskit.QuantumRegister(2)
    cr3 = qiskit.ClassicalRegister(2)
    qc3 = qiskit.QuantumCircuit(qr3, cr3)
    # Canonicalize second qubit using the correlation between the two
    # input basis states (|00> and |11>) via a CNOT with qubit0 as control.
    qc3.cx(qr3[0], qr3[1])     # CNOT
    # Map qubit0: |0> -> -|1>, |1> -> |0>
    qc3.x(qr3[0])              # X
    qc3.z(qr3[0])              # Z
    # Map qubit1 (now always |0>) to |->
    qc3.x(qr3[1])              # X
    qc3.h(qr3[1])              # H
    return qc3

if __name__ == "__main__":
    qc = create_circuit()
    print(qc)
