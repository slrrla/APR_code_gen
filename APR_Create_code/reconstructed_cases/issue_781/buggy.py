from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

theta = Parameter("$\\Theta$")
qc = QuantumCircuit(1)
qc.ry(theta, 0)

# Attempting to save circuit with free parameters using QASM,
# which does not tolerate unbound parameters.
qasm_str = qc.qasm()
with open("qc.qasm", "w") as qasm_file_write:
    qasm_file_write.write(qasm_str)
