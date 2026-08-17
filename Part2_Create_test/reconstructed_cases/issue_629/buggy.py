from qiskit import QuantumCircuit, execute, Aer, assemble, QuantumRegister, ClassicalRegister

qc = QuantumCircuit(2)
qc.x(0)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
print(qc.draw(output="text"))

sim = Aer.get_backend('qasm_simulator')
result = sim.run(qc).result()
counts = result.get_counts()
print(counts)
