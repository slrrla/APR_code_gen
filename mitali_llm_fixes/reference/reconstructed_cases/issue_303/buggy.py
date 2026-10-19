import qiskit
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
b = qiskit.circuit.ParameterVector('beta', 2)
a = qiskit.circuit.ParameterVector('alfa', 2)
d = qiskit.circuit.ParameterVector('delta', 1)

qc.rx(b[0], 0)
qc.rx(b[1], 1)
qc.ry(a[0], 0)
qc.ry(a[1], 1)
qc.rz(d[0], 0)

values = [1, 2, 3, 4, 5]
print(qc.parameters)
# assign_parameters binds values in alphabetical order of parameter names
# (alfa, beta, delta), NOT in the temporal order the gates were added
# (beta, alfa, delta) as the author expected.
qc.assign_parameters(values, inplace=True)
qc.draw("mpl")
