from qiskit import *
# FIX: Aer is no longer exported by qiskit -> import it from qiskit_aer, because Aer moved to the qiskit_aer package
from qiskit_aer import Aer

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

# FIX: removed execute() and no per-shot memory -> use simulator.run(transpile(...), memory=True), because execute was removed and memory=True stores each shot's raw outcome
job = simulator.run(transpile(circuit, simulator), shots=1024, memory=True)
# FIX: job.result(job) passed the job as a timeout and returned a Result summary -> job.result().get_memory(), because get_memory() returns the raw per-shot bits ('0'/'1')
a = job.result().get_memory()
print(a)
