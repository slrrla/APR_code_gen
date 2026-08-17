from math import pi
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import assemble, transpile
from qiskit.providers.aer import AerSimulator

backend = AerSimulator()

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.u(pi/2, pi/2, pi/2, qreg_q[0])
circuit.x(qreg_q[0])
circuit.y(qreg_q[0])
circuit.x(qreg_q[0])
circuit.y(qreg_q[0])
circuit.u(pi/2, pi/2, pi/2, qreg_q[0]).inverse()
circuit.measure(qreg_q[0], creg_c[0])

# Use optimization_level=0 to prevent transpilation from collapsing
# the circuit into an identity/empty circuit.
qobj = assemble(transpile(circuit, backend=backend, optimization_level=0), backend=backend)
job = backend.run(qobj)
result = job.result()
print(result.get_counts())
