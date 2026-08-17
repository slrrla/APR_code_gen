from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.providers.ibmq.managed import IBMQJobManager

backend = AerSimulator()

quanc_z = QuantumCircuit(1, 1)
quanc_z.h(0)
quanc_z.measure(0, 0)

quanc_x = QuantumCircuit(1, 1)
quanc_x.h(0)
quanc_x.measure(0, 0)

quanc_y = QuantumCircuit(1, 1)
quanc_y.h(0)
quanc_y.measure(0, 0)

job_manager = IBMQJobManager()

# meas_filter would normally come from qiskit-ignis measurement calibration
meas_filter = None

all_circuits = []
for _ in range(100):
    all_circuits.extend([quanc_z, quanc_x, quanc_y])

all_circuits = transpile(all_circuits, backend=backend)

MExperiments = job_manager.run(all_circuits, backend=backend, shots=1024, memory=True)

# Convert the ManagedResults into a plain Result so meas_filter.apply works,
# and so get_memory(i) can be used to index individual experiments.
managed_result = MExperiments.results()
results = meas_filter.apply(managed_result.combine_results())

# Use the circuit index (z, x, y repeating every 3 circuits) to separate
# the memory of each individual circuit instead of always fetching the
# first experiment's memory.
memory_z = []
memory_x = []
memory_y = []
for i in range(len(all_circuits)):
    mem = results.get_memory(i)
    if i % 3 == 0:
        memory_z.append(mem)
    elif i % 3 == 1:
        memory_x.append(mem)
    else:
        memory_y.append(mem)
