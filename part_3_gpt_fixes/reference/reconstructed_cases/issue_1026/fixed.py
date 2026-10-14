# Fixed for Qiskit >= 1.0: backend configuration/defaults must be obtained
# by calling backend.configuration() / backend.defaults(), not by accessing
# the private attributes directly.
import numpy as np
from qiskit import schedule, pulse
from qiskit.circuit import Parameter, QuantumCircuit, Gate
from warnings import filterwarnings
from qiskit.providers.fake_provider import FakeManilaV2

filterwarnings('ignore', category=DeprecationWarning)
filterwarnings('ignore', category=FutureWarning)

def get_qubit_freqs(backend):
    backend_defaults = backend.defaults()
    if backend_defaults is not None:
        return backend_defaults.qubit_freq_est
    else:
        n_qubits = backend.configuration().num_qubits
        keys = [f'wq{i}' for i in range(n_qubits)]
        return [backend.configuration().hamiltonian["vars"][key] for key in keys]

# select backend (local simulator standing in for a real IBM backend)
backend = FakeManilaV2()

print("backend name : {:}".format(backend.name))

# Backend parameters
dt = backend.configuration().dt
acquire_alignment = backend.configuration().timing_constraints['acquire_alignment']
granularity = backend.configuration().timing_constraints['granularity']
pulse_alignment = backend.configuration().timing_constraints['pulse_alignment']

# unit conversion factors -> all backend properties returned in SI (Hz, sec, etc.)
GHz = 1.0e9  # Gigahertz
MHz = 1.0e6  # Megahertz
us = 1.0e-6  # Microseconds
ns = 1.0e-9  # Nanoseconds

# We will find the qubit frequency for the following qubit.
qubit = 0
# The sweep will be centered around the estimated qubit frequency.
center_frequency_Hz = get_qubit_freqs(backend)[0]

# scale factor to remove factors of 10 from the data
scale_factor = 1e-7

# We will sweep 40 MHz around the estimated frequency in steps of 1 MHz.
frequency_span_Hz = 40 * MHz
frequency_step_Hz = 1 * MHz

frequency_min = center_frequency_Hz - frequency_span_Hz / 2
frequency_max = center_frequency_Hz + frequency_span_Hz / 2

frequencies_GHz = np.arange(frequency_min / GHz, frequency_max / GHz, frequency_step_Hz / GHz)

def get_closest_multiple_of(value, base_number):
    return int(value + base_number/2) - (int(value + base_number/2) % base_number)

def get_closest_multiple_of_granularity(num):
    return get_closest_multiple_of(num, granularity)

def get_dt_from(sec):
    lcm = np.lcm(acquire_alignment, pulse_alignment)
    return get_closest_multiple_of(sec/dt, lcm)

# Drive pulse parameters (us = microseconds)
drive_sigma_sec = 0.015 * us
drive_duration_sec = drive_sigma_sec * 8
drive_amp = 0.05

freq = Parameter('freq')
with pulse.build(backend=backend, default_alignment='sequential', name='Frequency sweep') as sweep_sched:
    drive_duration = get_closest_multiple_of_granularity(pulse.seconds_to_samples(drive_duration_sec))
    drive_sigma = pulse.seconds_to_samples(drive_sigma_sec)
    drive_chan = pulse.drive_channel(qubit)
    pulse.set_frequency(freq, drive_chan)
    pulse.play(pulse.Gaussian(duration=drive_duration, sigma=drive_sigma, amp=drive_amp,
                               name='freq_sweep_excitation_pulse'), drive_chan)

sweep_gate = Gate("sweep", 1, [freq])
qc_sweep = QuantumCircuit(1, 1)
qc_sweep.append(sweep_gate, [0])
qc_sweep.measure(0, 0)
qc_sweep.add_calibration(sweep_gate, (0,), sweep_sched, [freq])

frequencies_Hz = frequencies_GHz * GHz
exp_sweep_circs = [qc_sweep.assign_parameters({freq: f}, inplace=False) for f in frequencies_Hz]

sweep_schedule = schedule(exp_sweep_circs[0], backend)

num_shots_per_frequency = 1024
job = backend.run(exp_sweep_circs, meas_level=1, meas_return='avg', shots=num_shots_per_frequency)
frequency_sweep_results = job.result()

import matplotlib.pyplot as plt
sweep_values = []
for i in range(len(frequency_sweep_results.results)):
    res = frequency_sweep_results.get_memory(i) * scale_factor
    sweep_values.append(res[qubit])

plt.scatter(frequencies_GHz, np.real(sweep_values), marker='x', color='black')
plt.xlim([min(frequencies_GHz), max(frequencies_GHz)])
plt.xlabel("Frequency [GHz]")
plt.ylabel("Measured signal [a.u.]")
plt.show()
