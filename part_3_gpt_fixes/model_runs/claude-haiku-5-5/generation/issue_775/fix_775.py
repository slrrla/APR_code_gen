from qiskit import execute, Aer, QuantumCircuit

qasm_str = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
'''

# FIX: `execute` was given a raw QASM string instead of a circuit -> parse the string into a QuantumCircuit with `QuantumCircuit.from_qasm_str`, because `execute` only accepts circuit objects.
circuit = QuantumCircuit.from_qasm_str(qasm_str)
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend)
result = job.result()
print(result)
