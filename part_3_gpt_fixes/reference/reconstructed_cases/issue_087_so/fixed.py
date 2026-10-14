from qiskit import ClassicalRegister, QuantumRegister
from qiskit import QuantumCircuit, execute

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q)
qc.h(q[0])  # pylint: disable=no-member
qc.cx(q[0], q[1])  # pylint: disable=no-member
qc.measure(q, c)  # pylint: disable=no-member

job_sim = execute(qc, 'local_qasm_simulator')

sim_result = job_sim.result()

print(sim_result.get_counts(qc))
