from qiskit import QuantumCircuit, execute, Aer

# Build a small circuit (original question used 8 qubits, reduced here for practicality)
cir = QuantumCircuit(3)
cir.h(0)
cir.cx(0, 1)
cir.cx(1, 2)

backend = Aer.get_backend('unitary_simulator')
job = execute(cir, backend)

unitary = job.result().get_unitary(cir)
for row in unitary:
    print(row)
