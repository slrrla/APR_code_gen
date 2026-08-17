import numpy as np
from qiskit import QuantumCircuit, pulse
from qiskit.circuit import Gate, Parameter
from qiskit.pulse import DriveChannel, Gaussian
from qiskit.providers.fake_provider import FakeHanoi

backend = FakeHanoi()
backend_config = backend.configuration()

GHz = 1.0e9
NUM_SHOTS = 256

# Qubit chosen for calibration (deliberately NOT qubit 0)
qubit = 1

freq = Parameter('freq')

# Frequency sweep schedule for the chosen qubit
with pulse.build(backend=backend) as sweep_sched:
    pulse.set_frequency(freq, DriveChannel(qubit))
    pulse.play(Gaussian(duration=1600, amp=0.2, sigma=400), DriveChannel(qubit))

# FIX: build the circuit over all of the backend's qubits and target
# the actual `qubit` being calibrated, instead of assuming qubit 0.
n_bits = backend_config.n_qubits
sweep_gate = Gate("sweep", 1, [freq])
qc_sweep = QuantumCircuit(n_bits, 1)
qc_sweep.append(sweep_gate, [qubit])
qc_sweep.measure(qubit, 0)
qc_sweep.add_calibration(sweep_gate, (qubit,), sweep_sched, [freq])

# Create the frequency settings for the sweep (MUST BE IN HZ)
center_frequency_Hz = backend_config.qubit_freq_est[qubit]
frequencies_GHz = np.linspace(center_frequency_Hz / GHz - 0.02,
                               center_frequency_Hz / GHz + 0.02,
                               75)
frequencies_Hz = frequencies_GHz * GHz

exp_sweep_circs = [qc_sweep.assign_parameters({freq: f}, inplace=False)
                    for f in frequencies_Hz]

job = backend.run(exp_sweep_circs, meas_level=1, meas_return='avg', shots=NUM_SHOTS)
sweep_result = job.result(timeout=120)

sweep_values = []
for i in range(len(frequencies_Hz)):
    # FIX: `res` now has one entry per physical qubit on the backend,
    # so indexing by the actual `qubit` being calibrated is correct.
    res = sweep_result.get_memory(i) * 1e-14
    sweep_values.append(res[qubit])

print(sweep_values)
