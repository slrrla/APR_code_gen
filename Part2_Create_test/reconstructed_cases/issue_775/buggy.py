# Attempting to run an OpenQASM 2.0 program directly in Qiskit
from qiskit import execute, Aer

qasm_str = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
'''

backend = Aer.get_backend('qasm_simulator')
# Bug: passing the raw qasm text straight to execute instead of
# converting it into a QuantumCircuit first
job = execute(qasm_str, backend)
result = job.result()
print(result)
