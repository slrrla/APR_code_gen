from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error, ReadoutError

num_qubits = 5

# Manually define T1/T2 times (in ns) and gate time for each qubit
t1_times = [50e3, 60e3, 45e3, 55e3, 48e3]
t2_times = [30e3, 35e3, 28e3, 33e3, 29e3]
gate_time = 100  # ns

noise_model = NoiseModel()

for qubit in range(num_qubits):
    t1 = t1_times[qubit]
    t2 = t2_times[qubit]
    error = thermal_relaxation_error(t1, t2, gate_time)
    noise_model.add_quantum_error(error, ["id", "rz", "sx", "x"], [qubit])

    # Manually set a readout (measurement) error for each qubit
    p0given1 = 0.02
    p1given0 = 0.01
    readout_error = ReadoutError([[1 - p1given0, p1given0], [p0given1, 1 - p0given1]])
    noise_model.add_readout_error(readout_error, [qubit])

backend = AerSimulator(noise_model=noise_model)

qc = QuantumCircuit(num_qubits, num_qubits)
qc.h(0)
for i in range(num_qubits - 1):
    qc.cx(i, i + 1)
qc.measure(range(num_qubits), range(num_qubits))

transpiled = transpile(qc, backend)
result = backend.run(transpiled).result()
print(result.get_counts())
