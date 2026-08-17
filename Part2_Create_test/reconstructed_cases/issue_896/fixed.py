from qiskit import QuantumCircuit, execute, BasicAer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

def teleported_circuit(code):
    qreg_q = QuantumRegister(3, 'q')
    creg_c = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(qreg_q, creg_c)
    if code == 1:
        circuit.x(qreg_q[0])
    circuit.barrier(range(3))
    circuit.h(qreg_q[1])
    circuit.cx(qreg_q[1], qreg_q[2])
    circuit.cx(qreg_q[0], qreg_q[1])
    circuit.h(qreg_q[0])
    circuit.barrier(range(3))
    circuit.cx(qreg_q[1], qreg_q[2])
    circuit.cz(qreg_q[0], qreg_q[2])
    circuit.measure(qreg_q[2], creg_c[0])

    backend = BasicAer.get_backend('statevector_simulator')
    job = execute(circuit, backend, shots=1)
    return job.result().get_counts()

#### Example ####
code_string = [1, 0, 0, 1, 1, 1]
teleported_code = [teleported_circuit(code_string[i]) for i in range(len(code_string))]
print('Here is your telported code:', teleported_code)
