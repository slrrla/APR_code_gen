from qiskit import QuantumCircuit, Aer, execute

gamma, beta, delta = 0.1, 0.2, 0.3
simulator = Aer.get_backend('qasm_simulator')

# Circ 1
quancs = QuantumCircuit(1)
quancs.u3(gamma, beta, delta, 0)

# Circ 2
quancs1 = QuantumCircuit(1)
quancs1.u3(2, 3, 2, 0)
quancs1.u3(gamma, beta, delta, 0)

# Circuit 3
quancs2 = QuantumCircuit(1)
quancs2.u3(-2.5, 2, -2, 0)
quancs2.u3(gamma, beta, delta, 0)

results = execute(quancs, simulator).result()
results1 = execute(quancs1, simulator).result()
results2 = execute(quancs2, simulator).result()
