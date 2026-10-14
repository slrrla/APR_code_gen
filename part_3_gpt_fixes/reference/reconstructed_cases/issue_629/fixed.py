from qiskit import QuantumCircuit, execute, Aer, assemble, QuantumRegister, ClassicalRegister

qc = QuantumCircuit(2)
qc.x(0)
qc.h(0)
qc.cx(0, 1)

# Check the statevector before measurement to correctly interpret qubit ordering
sv_sim = Aer.get_backend('statevector_simulator')
sv_result = sv_sim.run(qc).result()
print(sv_result.get_statevector())

qc.measure_all()
print(qc.draw(output="text"))

sim = Aer.get_backend('qasm_simulator')
result = sim.run(qc).result()
counts = result.get_counts()
print(counts)
