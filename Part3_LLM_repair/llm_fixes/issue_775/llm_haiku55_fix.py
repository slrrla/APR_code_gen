# FIX: QuantumCircuit was not imported -> added QuantumCircuit to the import, because the string must be parsed into a circuit object
from qiskit import QuantumCircuit, execute, Aer

qasm_str = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
'''

# FIX: execute() was given the raw QASM string -> parse it with QuantumCircuit.from_qasm_str, because execute() requires a QuantumCircuit object
circuit = QuantumCircuit.from_qasm_str(qasm_str)
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend)
result = job.result()
print(result)
