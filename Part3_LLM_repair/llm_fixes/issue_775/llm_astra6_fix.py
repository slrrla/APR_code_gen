# FIX: OpenQASM text must be parsed into a circuit -> import QuantumCircuit, because it provides the OpenQASM 2.0 parser.
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
# FIX: execute received raw OpenQASM text -> parse it into a QuantumCircuit, because execute expects a circuit rather than a string.
job = execute(QuantumCircuit.from_qasm_str(qasm_str), backend)
result = job.result()
print(result)

