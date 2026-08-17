from qiskit import *
from qiskit.compiler import transpile, assemble
from qiskit import IBMQ
from qiskit import QuantumCircuit, execute, BasicAer
import logging

logging.basicConfig(filename='log', level=logging.DEBUG)

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')

# SELECT A BACKEND
backend = provider.get_backend('ibmq_qasm_simulator')

# ALGO
qr = QuantumRegister(3)
cr = ClassicalRegister(3)
circuit = QuantumCircuit(qr, cr)
circuit.x(qr[0])
circuit.x(qr[1])
circuit.ccx(qr[0], qr[1], qr[2])
circuit.cx(qr[0], qr[1])
circuit.measure(qr, cr)

print('About to run job')
job = execute(circuit, backend)
print('Job Finished')
result = job.result()
counts = result.get_counts(circuit)
print(counts)
