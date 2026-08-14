from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Estimator
from qiskit.quantum_info import SparsePauliOp

# Define the base circuit
qc = QuantumCircuit(3)
qc.h(2)
qc.cx(2, 1)
qc.x(0)
qc.cx(0, 2)

# Define the measurement circuit
# It transforms Z basis to X basis
qc_mes = QuantumCircuit(3)
qc_mes.h(0)
qc_mes.h(1)
qc_mes.h(2)

# Combine base with measurement circuit
qc_all = qc.copy()
qc_all.compose(qc_mes, inplace=True)

num_shots = 10000
backend = AerSimulator(method="statevector")

# Use estimator to run the circuit
estimator = Estimator(backend, options={"default_shots": int(1e4)})
op = SparsePauliOp.from_list(
    [
        ("XXX", (-105.8)),
    ]
)
job = estimator.run([(qc, op)])
measured_energy = job.result()[0].data.evs
print('estimator expectation val:', measured_energy)

# Use simulator to run the circuit
qc_all.measure_all()
job2 = backend.run(qc_all, shots=num_shots)
job2_res = job2.result().get_counts()
exp_cal = 0
for key, val in job2_res.items():
    if key.count('1') % 2 == 0:
        exp_cal += val
    else:
        exp_cal -= val
exp_cal = exp_cal * (-105.8) / num_shots
print('calculated expectation val:', exp_cal)
