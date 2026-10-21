from qiskit import *

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

job = execute(circuit, backend=simulator, shots=1024)
# FIX: job.result(job) passed the job as an unexpected argument -> changed to job.result() with no arguments, because Job.result() takes none
a = job.result()
# FIX: print(a) printed the whole Result object instead of raw data -> print(a.get_counts()) to output the measured counts, because the user wants the 0/1 outcomes
print(a.get_counts())
