# FIX: `execute` and `qiskit.Aer` were removed in Qiskit 1.x -> import QuantumCircuit/transpile and Aer from qiskit_aer, because the old import fails and the QASM string must be parsed into a circuit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

qasm_str = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
'''

backend = Aer.get_backend('qasm_simulator')
# FIX: a raw OpenQASM string was passed to execute -> parse it with QuantumCircuit.from_qasm_str and run the transpiled circuit, because backends only accept QuantumCircuit objects, not QASM text
job = backend.run(transpile(QuantumCircuit.from_qasm_str(qasm_str), backend))
result = job.result()
print(result)
