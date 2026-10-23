from qiskit import *

simulator = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(1)
cr = ClassicalRegister(1)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.measure(qr, cr)

# FIX: Individual shot outcomes were not saved -> enable memory, because raw measurement data requires it.
job = execute(circuit, backend=simulator, shots=1024, memory=True)
# FIX: result(job) does not extract measurement data -> use result().get_memory(circuit), because it returns the '0' or '1' outcome for each shot.
a = job.result().get_memory(circuit)
print(a)

