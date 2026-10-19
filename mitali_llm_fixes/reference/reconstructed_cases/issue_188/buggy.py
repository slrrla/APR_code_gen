import math
from qiskit import BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.visualization import plot_histogram
from qiskit.test.mock import FakeVigo

pi = math.pi

def oracle(circuit, qr):
    circuit.x(qr[0])
    circuit.x(qr[2])
    circuit.x(qr[3])
    circuit.cu1(pi/4, qr[0], qr[3])
    circuit.cx(qr[0], qr[1])
    circuit.cu1(-pi/4, qr[1], qr[3])
    circuit.cx(qr[0], qr[1])
    circuit.cu1(pi/4, qr[1], qr[3])
    circuit.cx(qr[1], qr[2])
    circuit.cu1(-pi/4, qr[2], qr[3])
    circuit.cx(qr[0], qr[2])
    circuit.cu1(pi/4, qr[2], qr[3])
    circuit.cx(qr[1], qr[2])
    circuit.cu1(-pi/4, qr[2], qr[3])
    circuit.cx(qr[0], qr[2])
    circuit.cu1(pi/4, qr[2], qr[3])
    circuit.x(qr[0])
    circuit.x(qr[2])
    circuit.x(qr[3])

def amplification(circuit, qr):
    circuit.h(qr)
    circuit.x(qr)
    circuit.cu1(pi/4, qr[0], qr[3])
    circuit.cx(qr[0], qr[1])
    circuit.cu1(-pi/4, qr[1], qr[3])
    circuit.cx(qr[0], qr[1])
    circuit.cu1(pi/4, qr[1], qr[3])
    circuit.cx(qr[1], qr[2])
    circuit.cu1(-pi/4, qr[2], qr[3])
    circuit.cx(qr[0], qr[2])
    circuit.cu1(pi/4, qr[2], qr[3])
    circuit.cx(qr[1], qr[2])
    circuit.cu1(-pi/4, qr[2], qr[3])
    circuit.cx(qr[0], qr[2])
    circuit.cu1(pi/4, qr[2], qr[3])
    circuit.x(qr)
    circuit.h(qr)

qr = QuantumRegister(4)
cr = ClassicalRegister(4)
iterations = 1
groverCircuit = QuantumCircuit(qr, cr)

# apply Hadamard gate to all qubits
groverCircuit.h(qr)

while iterations > 0:
    oracle(groverCircuit, qr)
    amplification(groverCircuit, qr)
    iterations -= 1

# measure
groverCircuit.measure(qr, cr)

# stand-in for a real IBMQ backend (e.g. ibmqx2) - local simulator only, no network calls
backend = FakeVigo()
# backend = BasicAer.get_backend('qasm_simulator')
shots = 1024
results = execute(groverCircuit, backend=backend, shots=shots).result()
answer = results.get_counts()
print(answer)
print(plot_histogram(answer))
