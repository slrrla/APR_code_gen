from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
from qiskit.providers.aer.noise import NoiseModel

qubit_count = 3
q = QuantumRegister(qubit_count)
c = ClassicalRegister(qubit_count)
circuits = []
for ghz_size in range(2, qubit_count + 1):
    qc = QuantumCircuit(q, c)
    qc.h(q[0])
    for s in range(ghz_size - 1):
        qc.cx(q[s], q[s + 1])
    qc.barrier()
    qc.measure(q, c)
    circuits.append(qc)

pm = PassManager()
pm.append(Unroller(['u1', 'u2', 'u3', 'cx', 'id']))

backend = Aer.get_backend('qasm_simulator')
noise_model = NoiseModel.from_backend(backend)  # placeholder noise model

shots = 1024
num_sims_per_model = 1
c_idx = 0
nm = 0

sim_data_sets = {}
labels = ['2-qubit Average Model']
for l in labels:
    sim_data_sets[l] = []

for s in range(num_sims_per_model):
    job_sim = execute(
        circuits[c_idx],
        backend,
        shots=shots,
        pass_manager=pm,
        optimization_level=0,
        noise_model=noise_model,
        # basis_gates=noise_model.basis_gates
    )
    result_sim = job_sim.result()
    print(result_sim.get_counts())
