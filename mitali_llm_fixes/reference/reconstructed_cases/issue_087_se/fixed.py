import numpy as np
from qiskit.providers.fake_provider import FakeManila
from qiskit import transpile

backend = FakeManila()
# 1.1. retrieve the configuration for the backend
config = backend.configuration()
# 1.2. retrieve the default values for the backend
defaults = backend.defaults()

### 2. Qubit SPECTROSCOPY ###
QUBIT = 1

# unit conversion factors (All backend properties are in SI units)
GHz = 1.0e9  # Gigahertz
MHz = 1.0e6  # Megahertz
us = 1.0e-6  # Microseconds
ns = 1.0e-9  # Nanoseconds

# experiment options
from collections import namedtuple

drive_sigma_sec = 0.015 * us  # width of the gaussian pulse
drive_duration_sec = drive_sigma_sec * 8  # truncating the gaussian to 8 sigma

Experiment_options = namedtuple("Experiment_options", "amp, sigma, width, duration")
experiment_options = Experiment_options(
    amp=0.05,  # The amplitude of the spectroscopy pulse
    duration=drive_duration_sec,  # The duration of the spectroscopy pulse in seconds
    sigma=drive_sigma_sec,  # The standard deviation of the spectroscopy pulse in seconds
    width=0,  # The width of the flat-top of the GaussianSquare pulse in samples
)

# Retrieve the estimated qubit frequency
center_frequency = defaults.qubit_freq_est[QUBIT]  # in Hz
print(f"Qubit {QUBIT} has an estimated frequency of {center_frequency/GHz} GHz")

# Create a range to sweep
frequency_span = 40 * MHz  # in Hz
frequency_step = 1 * MHz  # in Hz
frequency_min = center_frequency - frequency_span / 2
frequency_max = center_frequency + frequency_span / 2
frequency_list = np.arange(frequency_min, frequency_max, frequency_step)

# set timing options for experiment
from qiskit_experiments.framework import BackendTiming

timing = BackendTiming(backend)
duration = timing.round_pulse(time=experiment_options.duration)  # the duration regarding to timing constraints
sigma = experiment_options.sigma / timing.dt
width = experiment_options.width / timing.dt

### 2. Create a spectroscopy schedule
from qiskit import pulse
from qiskit.circuit import Parameter  # This is Parameter class for variable parameters
from qiskit.circuit import Gate, QuantumCircuit

# 2.1 create variable parameter
freq_param = Parameter("frequency")

# 2.2 create a default pulse schedule
with pulse.build(backend=backend, name="spectroscopy") as spec_sched:
    # 2.2.1 choose drive channel
    drive_chan = pulse.drive_channel(QUBIT)
    # 2.2.2 change frequency on selected channel
    pulse.shift_frequency(freq_param, drive_chan)
    # 2.2.3 Play pulse
    pulse.play(
        pulse=pulse.GaussianSquare(
            duration=duration,
            sigma=sigma,
            width=width,
            amp=experiment_options.amp,
        ),
        channel=drive_chan,
    )
    # 2.2.4 shift frequency back to original value
    pulse.shift_frequency(-freq_param, drive_chan)

# 2.3 Create the Spectroscopy gate
spec_gate_name = "Spec_gate"
spec_gate = Gate(name=spec_gate_name, num_qubits=1, params=[freq_param])

# 2.4 Create a quantum circuit for spectroscopy
qc_spec = QuantumCircuit(1)
qc_spec.append(spec_gate, (0,))  # apply the spectroscopy gate to qubit register 0

# Adds measurement to all non-idle qubits.
qc_spec.measure_active()

# 2.5 add circuit calibration
qc_spec.add_calibration(
    spec_gate_name,
    qubits=[QUBIT,],
    schedule=spec_sched,
    params=[freq_param],
)

# 2.6 apply parameters
freq_sweep_circs = [
    qc_spec.assign_parameters({freq_param: round(f, 3)}, inplace=False)
    for f in frequency_list
]

# Transpile the circuits for the target backend so the custom calibrated
# gate is recognized and not lowered into unsupported basis gates.
freq_sweep_circs = transpile(freq_sweep_circs, backend)

### Get Results ###
num_shots_per_frequency = 1024
job = backend.run(
    freq_sweep_circs,
    meas_level=1,
    meas_return="avg",
    shots=num_shots_per_frequency,
)
frequency_sweep_results = job.result()
