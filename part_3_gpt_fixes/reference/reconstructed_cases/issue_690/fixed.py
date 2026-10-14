from qiskit import IBMQ, Aer, QuantumCircuit, execute

qc = QuantumCircuit(2)
qc.h([0, 1])
qc.measure_all()

job = execute(qc, Aer.get_backend('qasm_simulator'), shots=4321)
print('States observed upon measurement:', job.result().get_counts())
