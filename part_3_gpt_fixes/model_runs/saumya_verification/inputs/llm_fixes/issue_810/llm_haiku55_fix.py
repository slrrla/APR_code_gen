from qiskit import *

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

job = execute(circuit, backend=simulator, shots=1024)
# FIX: job.result(job) passed the job as an argument to result(), which takes none, and printed the Result object instead of the data -> call job.result() with no arguments and extract counts with get_counts(), because that returns the raw measurement counts
a = job.result().get_counts()
print(a)
