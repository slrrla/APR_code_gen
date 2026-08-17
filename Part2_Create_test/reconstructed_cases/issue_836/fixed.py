import time
import numpy as np
from qiskit import QuantumCircuit, Parameter, assemble
from qiskit.providers.aer import Aer

n_params = 3
n_reps = 5
N_shots = 1e6

all_qiskit_params = [Parameter(f'theta{i}') for i in range(n_params)]
all_param_values = np.random.rand(n_params, n_reps)

mapped_circuit = QuantumCircuit(1, 1)
for p in all_qiskit_params:
    mapped_circuit.rx(p, 0)
mapped_circuit.measure(0, 0)

backend = Aer.get_backend('aer_simulator')

qobj = assemble(
    [mapped_circuit.bind_parameters(dict(zip(all_qiskit_params, all_param_values[:, pp])))
     for pp in range(n_reps)],
    backend=backend, shots=N_shots)

# backend.run() only submits the job and returns almost immediately
start_run = time.time()
job = backend.run(qobj)
print("backend.run() took", time.time() - start_run, "seconds")

# job.result() blocks until the simulation actually finishes, so its
# runtime is expected to scale with N_shots -- this is not a bug
start_result = time.time()
counts = job.result().get_counts()
print("job.result() took", time.time() - start_result, "seconds")
