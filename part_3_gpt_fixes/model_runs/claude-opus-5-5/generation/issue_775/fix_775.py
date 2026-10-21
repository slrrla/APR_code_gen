# FIX: QuantumCircuit was not imported -> added it to the import, because it is needed to parse the QASM string
from qiskit import execute, Aer, QuantumCircuit

qasm_str = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
'''

backend = Aer.get_backend('qasm_simulator')
# FIX: a raw QASM string was passed to execute -> parse it with QuantumCircuit.from_qasm_str, because execute only accepts QuantumCircuit objects
job = execute(QuantumCircuit.from_qasm_str(qasm_str), backend)
result = job.result()
print(result)
