from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# https://github.com/Qiskit/qiskit-ibm-runtime
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# Save an IBM Cloud account.
QiskitRuntimeService.save_account(channel="ibm_quantum", token="Add_your_key", overwrite=True)

# Read default credentials from disk
service = QiskitRuntimeService(channel='ibm_quantum', instance="ibm-q/open/main")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
print(qc.draw())

# Optimize problem for quantum execution
backend = service.least_busy(operational=True, simulator=False)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)

sampler = Sampler(mode=backend)
sampler.options.default_shots = 100000
job = sampler.run([isa_circuit])
print(f"Job ID is {job.job_id()}")

pub_result = job.result()[0]
print(f"Counts for the meas output register: {pub_result.data.meas.get_counts()}")
