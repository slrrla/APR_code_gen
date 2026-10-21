from qiskit import *
# FIX: Aer is no longer importable from qiskit -> import it from qiskit_aer, because Aer was moved to the separate qiskit_aer package
from qiskit_aer import Aer

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

# FIX: removed execute() and no per-shot memory requested -> use simulator.run on the transpiled circuit with memory=True, because execute was removed and memory=True makes the backend keep every shot's raw bit
job = simulator.run(transpile(circuit, simulator), shots=1024, memory=True)
# FIX: job.result(job) passed job as the timeout and returned only the Result summary -> job.result().get_memory(), because get_memory() returns the raw list of measured '0'/'1' outcomes per shot
a = job.result().get_memory()
print(a)
