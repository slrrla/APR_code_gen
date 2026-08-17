import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.tools.monitor import job_monitor

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

# FIX: combine all circuits into a single list and run them in one job.
# transpile is skipped here since execute() performs it internally.
all_circuits = []
for i in range(10):
    all_circuits += circuits[i][:]

qjob = execute(all_circuits, shots=nshot, backend=backend)
job_monitor(qjob)
result = qjob.result()

counts = []
for i in range(10):
    count_i = []
    for j in range(nuni):
        count_i.append(result.get_counts(all_circuits[(nuni * i) + j]))
    counts.append(count_i)
