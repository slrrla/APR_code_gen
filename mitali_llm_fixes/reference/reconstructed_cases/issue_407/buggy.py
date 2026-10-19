import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, transpile, Aer

# Local simulator instead of a real/hardware backend
backend = Aer.get_backend('qasm_simulator')

qrz = QuantumRegister(1)
crz = ClassicalRegister(1)

def qc(e):
    # qc is a function with both parameters and random numbers.
    circuit = QuantumCircuit(qrz, crz)
    circuit.rx(e, 0)
    circuit.measure(qrz, crz)
    return circuit

E = np.linspace(-5, 5, 10)  # Parameters
circuits = []
nuni = 10  # Number of the circuits in each set.
nshot = 100

for i in range(10):
    circuitsi = []
    for j in range(nuni):
        circuit = qc(E[i])  # qc is a function with both parameters and random numbers.
        circuitsi.append(circuit)
    circuits.append(circuitsi)

for i in range(len(circuits)):
    for j in range(nuni):
        circuits[i][j] = transpile(circuits[i][j], backend=backend)

# BUG: running each set of circuits separately instead of combining them
counts = []
for i in range(10):
    job = execute(circuits[i], backend=backend, shots=nshot)
    result = job.result()
    count_i = []
    for j in range(nuni):
        count_i.append(result.get_counts(circuits[i][j]))
    counts.append(count_i)
