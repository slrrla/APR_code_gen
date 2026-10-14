from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
import numpy as np

theta = np.pi / 3  # unknown angle we want to estimate

q = QuantumRegister(1, 'q')
c = ClassicalRegister(1, 'c')

# Experiment 1: rotate to measure <X> = P(0) - P(1)
circuit_experiment_1 = QuantumCircuit(q, c)
circuit_experiment_1.h(q[0])
circuit_experiment_1.u1(theta, q[0])
circuit_experiment_1.h(q[0])
circuit_experiment_1.measure(q[0], c[0])

# Experiment 2: rotate to measure <Y> = P'(0) - P'(1)
circuit_experiment_2 = QuantumCircuit(q, c)
circuit_experiment_2.h(q[0])
circuit_experiment_2.u1(theta, q[0])
circuit_experiment_2.sdg(q[0])
circuit_experiment_2.h(q[0])
circuit_experiment_2.measure(q[0], c[0])

backend = Aer.get_backend('qasm_simulator')
shots = 8192

job1 = execute(circuit_experiment_1, backend, shots=shots)
counts1 = job1.result().get_counts(circuit_experiment_1)
p0_1 = counts1.get('0', 0) / shots
p1_1 = counts1.get('1', 0) / shots
exp_x = p0_1 - p1_1

job2 = execute(circuit_experiment_2, backend, shots=shots)
counts2 = job2.result().get_counts(circuit_experiment_2)
p0_2 = counts2.get('0', 0) / shots
p1_2 = counts2.get('1', 0) / shots
exp_y = p0_2 - p1_2

estimated_theta = np.sign(exp_y) * np.arccos(np.clip(exp_x, -1, 1))
print("Estimated theta:", estimated_theta, "True theta:", theta)
