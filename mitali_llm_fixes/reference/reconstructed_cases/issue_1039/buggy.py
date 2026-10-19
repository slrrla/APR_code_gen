from qiskit import QuantumCircuit, BasicAer, execute

qc = QuantumCircuit(3)
qc.h(0)
qc.cx([0, 0], [1, 2])

backend_sv = BasicAer.get_backend('statevector_simulator')
job = execute(qc, backend_sv, shots=1024)
result = job.result()
sv_ev = result.get_statevector(qc)
print(sv_ev)
