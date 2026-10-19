from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute
from qiskit import Aer

qr = QuantumRegister(4, 'q')
cr = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qr, cr)

circuit.h(qr[0])
circuit.h(qr[2])
circuit.cx(qr[0], qr[1])
circuit.cx(qr[2], qr[3])
circuit.measure(qr, cr)

backend = Aer.get_backend('qasm_simulator')

# Runs without any optimization, so parallelizable gates are not
# necessarily scheduled to run at the same time.
job = execute(circuit, backend)
result = job.result()
print(result.get_counts(circuit))
