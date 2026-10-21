from qiskit import execute, Aer
from qiskit import QuantumCircuit

qasm_str = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
'''

backend = Aer.get_backend('qasm_simulator')
# FIX: passed a raw QASM string to execute -> build a QuantumCircuit with from_qasm_str first, because execute needs a circuit object, not a string
qc = QuantumCircuit.from_qasm_str(qasm_str)
job = execute(qc, backend)
result = job.result()
print(result)
