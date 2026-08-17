import qiskit
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)

# Name parameters with a slice-number prefix so that alphabetical
# ordering (which is how Qiskit always assigns values) matches the
# temporal order of the circuit. Barriers stop the compiler from
# reordering operations across timeslices.
p_b0 = qiskit.circuit.Parameter('0_beta0')
p_b1 = qiskit.circuit.Parameter('0_beta1')
p_a0 = qiskit.circuit.Parameter('1_alfa0')
p_a1 = qiskit.circuit.Parameter('1_alfa1')
p_d0 = qiskit.circuit.Parameter('2_delta0')

qc.rx(p_b0, 0)
qc.rx(p_b1, 1)
qc.barrier()
qc.ry(p_a0, 0)
qc.ry(p_a1, 1)
qc.barrier()
qc.rz(p_d0, 0)

values = [1, 2, 3, 4, 5]
print(qc.parameters)
qc.assign_parameters(values, inplace=True)
qc.draw("mpl")
