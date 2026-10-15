from qiskit import *

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

job = execute(circuit, backend=simulator, shots=1024)
# FIX: job.result(job) passed a bogus argument and returned the Result object -> call job.result().get_counts(), because result() takes no argument and get_counts() returns the raw measurement counts
a = job.result().get_counts()
print(a)
