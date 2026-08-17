from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from numpy import pi

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])

backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, Aer.get_backend('qasm_simulator'), shots=20000, memory=True)

output = []
result_list = job.result().get_memory()
for entry in result_list:
    output.append(int(entry))
print(output)
