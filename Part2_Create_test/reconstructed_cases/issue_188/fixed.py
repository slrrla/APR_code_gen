import math
from qiskit import BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, transpile, assemble
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

# local simulator standing in for the ibmq_vigo backend, exposing its
# basis_gates and coupling_map so we can see the real transpiled cost
backend = FakeVigo()
shots = 1024
groverCircuit_transpiled = transpile(groverCircuit, backend, optimization_level=3)
qobj = assemble(groverCircuit_transpiled, backend=backend, shots=shots)
results = backend.run(qobj).result()
answer = results.get_counts()
print("%d depth, %d CNOTs" % (groverCircuit.depth(), groverCircuit.count_ops()['cx']))
print("%d depth, %d CNOTs" % (groverCircuit_transpiled.depth(), groverCircuit_transpiled.count_ops()['cx']))
print(answer)
plot_histogram(answer)
