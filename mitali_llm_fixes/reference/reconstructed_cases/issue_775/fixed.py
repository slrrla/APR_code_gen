from qiskit import QuantumCircuit, execute, Aer

qasm_str = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
'''

qc = QuantumCircuit.from_qasm_str(qasm_str)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)
result = job.result()
print(result)
