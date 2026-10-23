from qiskit import *

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

job = execute(circuit, backend=simulator, shots=100)
result = job.result()
counts_dict = result.get_counts()
print(counts_dict)
