import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

qr = QuantumRegister(2, name="q")
cr = ClassicalRegister(2, 'c')
fivequbitcircuit = QuantumCircuit(qr, cr)

fivequbitcircuit.initialize("1", [0])  # initializing the first qubit to 1
fivequbitcircuit.initialize("1", [1])  # initializing the second qubit to 1

fivequbitcircuit.measure(qr, cr)

# Drawing the Quantum Circuit
fivequbitcircuit.draw('mpl')

from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram

backend = Aer.get_backend("aer_simulator")
tqc = transpile(fivequbitcircuit, backend)
job = backend.run(tqc, shots=1000)
result = job.result()
counts = result.get_counts(tqc)
plot_histogram(counts)
