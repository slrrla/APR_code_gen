from qiskit import *

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

job = execute(circuit, backend=simulator, shots=1024)
# FIX: job.result(job) passed the job as a timeout and printed the Result object -> call job.result().get_counts(circuit), because this returns the raw counts dictionary
a = job.result().get_counts(circuit)
print(a)
