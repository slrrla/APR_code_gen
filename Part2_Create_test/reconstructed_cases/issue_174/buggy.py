from qiskit import QuantumCircuit, execute
from qiskit import BasicAer as Aer

# Attempt to condition a gate on a single bit of a classical register
# using indexing inside the OpenQASM 2 "if" statement (c[0]==1).
# OpenQASM 2 does not support indexing the classical register in an
# "if" statement -- only whole-register integer comparisons are allowed.
cloner1 = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg c[1];
x q[2];
x q[4];
x q[0]; //Set up input
measure q[0] -> c[0];
if (c[0]==1) CX q[1],q[2];
if (c[0]==1) CX q[2],q[1];
if (c[0]==1) CX q[1],q[2];
if (c[0]==1) CX q[3],q[4];
if (c[0]==1) CX q[4],q[3];
if (c[0]==1) CX q[3],q[4];
measure q[1]->c[0];
measure q[3]->c[0];
"""

circuit = QuantumCircuit.from_qasm_str(cloner1)

backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()
print(result.get_counts())
