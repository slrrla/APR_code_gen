from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, IBMQ, execute
from numpy import pi

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])

# IBMQ.save_account(TOKEN)  # only needs to be done once
IBMQ.load_account()  # Load account from disk

provider = IBMQ.get_provider(hub='ibm-q', group='open')
backend = provider.get_backend('ibmq_vigo')

job = execute(circuit, backend, shots=20000, memory=True)

output = []
result_list = job.result().get_memory()
for entry in result_list:
    output.append(int(entry))
print(output)
