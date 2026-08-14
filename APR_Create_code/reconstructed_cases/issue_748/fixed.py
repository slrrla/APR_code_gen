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

# Use optimization_level=3 so the transpiler schedules independent
# gates (like the two cx gates) to run in parallel where possible.
job = execute(circuit, backend, optimization_level=3)
result = job.result()
print(result.get_counts(circuit))
