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

MExperiments = job_manager.run(all_circuits, backend=backend, shots=1024)

# BUG: meas_filter.apply expects a Result, not a ManagedResults object
results = meas_filter.apply(MExperiments.results())

# BUG: get_memory() is called without an index, so it always returns the
# same (first) experiment's memory for all three labels
memory_z = results.get_memory()
memory_x = results.get_memory()
memory_y = results.get_memory()
