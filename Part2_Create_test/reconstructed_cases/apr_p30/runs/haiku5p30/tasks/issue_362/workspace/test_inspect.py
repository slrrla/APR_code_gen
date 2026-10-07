from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(0)

backend = AerSimulator(method='unitary')
job = backend.run(circuit).result()

print("Number of experiments:", len(job.results))
print("\nFirst result data:", job.results[0].data)
print("First result data type:", type(job.results[0].data))
print("First result data dict:", vars(job.results[0].data))

# Try using the data method
print("\nUsing data() method:", job.data(0))
