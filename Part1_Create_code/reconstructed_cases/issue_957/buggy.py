import qiskit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer

def I(input):
    q = QuantumRegister(1)
    c = ClassicalRegister(1)
    qc = QuantumCircuit(q, c)
    if input == '1':  # if input = 1, initialize the qubit to 1
        qc.x(q[0])
    qc.iden(q[0])
    qc.measure(q[0], c[0])
    backend = Aer.get_backend('statevector_simulator')
    result = qiskit.execute(qc, backend=backend, shots=1).result()
    output = result.data(qc)
    return output

print('\nResults for the Iden gate')
for input in ['0', '1']:
    print(' Input', input, 'gives output', I(input))
