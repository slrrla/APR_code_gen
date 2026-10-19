from qiskit import QuantumRegister, ClassicalRegister, assemble, Aer
from qiskit import QuantumCircuit, execute, IBMQ
from qiskit.tools.monitor import job_monitor

backend = Aer.get_backend('aer_simulator')
q = QuantumRegister(3, 'q')
c = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(q, c)

circuit.h(q[0])
circuit.x(q[0])
circuit.y(q[0])
circuit.z(q[0])
circuit.x(q[1])
circuit.h(q[1])
circuit.z(q[1])
circuit.y(q[2])

# circuit.measure(q,c)  <- remove measurement so the statevector reflects the full superposition

job = execute(circuit, backend, shots=1024)
# counts = job.result().get_counts()  <- this won't work without measurement

circuit.save_statevector()
qobj = assemble(circuit)
state = backend.run(qobj).result().get_statevector()

# print(counts)  <- this neither
print(state)
