from qiskit import QuantumCircuit, QuantumRegister

q = QuantumRegister(8, 'q')
qp = QuantumCircuit(q)

# Block A for the first time step
qp.cx(q[0], q[1])
qp.cx(q[2], q[3])
qp.cx(q[4], q[5])
qp.cx(q[6], q[7])

qp.barrier()

# Block B for the second time step
qp.cx(q[1], q[2])
qp.cx(q[3], q[4])
qp.cx(q[5], q[6])

print(qp)
