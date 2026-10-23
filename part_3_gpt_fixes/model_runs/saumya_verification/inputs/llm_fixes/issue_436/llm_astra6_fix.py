from qiskit import pulse, assemble
from qiskit.pulse import Play, Schedule, DriveChannel, Gaussian, AcquireChannel, Waveform
from qiskit.providers.aer import PulseSimulator
from qiskit.test.mock import FakeArmonk
import numpy as np

job_params = {
    'meas_level': 1,
    'meas_return': 'avg',
    'shots': 512
}
spec_range = 0.300
num_spec01_freqs = 71
GHz = 1.0e9

def get_exc_chans(gv):
    return [AcquireChannel(i) for i in range(gv['backend_config'].n_qubits)]

def get_spec01_freqs(center_freqs, qubit):
    center_freq = round(center_freqs[qubit], -8)
    return np.linspace(center_freq/GHz - spec_range/2,
                        center_freq/GHz + spec_range/2,
                        num_spec01_freqs)

backend_real = FakeArmonk()
backend = PulseSimulator.from_backend(backend_real)
qubit = 0
backend_config = backend.configuration()
exc_chans = get_exc_chans(globals())
dt = backend_config.dt
backend_defaults = backend.defaults()
center_frequency = backend_defaults.qubit_freq_est
inst_sched_map = backend_defaults.instruction_schedule_map

meas = inst_sched_map.get('measure', qubits=[qubit])

drive_amp = 0.25
drive_duration = inst_sched_map.get('x', qubits=[qubit]).duration
drive_sigma = drive_duration // 4
spec_pulse = Gaussian(duration=drive_duration, amp=drive_amp, sigma=drive_sigma,
                       name=f"Spec drive amplitude = {drive_amp}")

spec_freqs_GHz = get_spec01_freqs(center_frequency, qubit)

spec01_scheds = []
for freq in spec_freqs_GHz:
    with pulse.build(name="Spec Pulse at %.3f GHz" % freq) as spec01_sched:
        with pulse.align_sequential():
            # FIX: PulseSimulator does not support set_frequency -> modulate waveform samples by exp(2j*pi*(target-LO)*t), because this supplies the frequency offset in Hz at sample times in seconds.
            pulse.play(Waveform(spec_pulse.get_waveform().samples * np.exp(2j * np.pi * (freq*GHz - center_frequency[qubit]) * np.arange(drive_duration) * dt)), DriveChannel(qubit))
            pulse.call(meas)
    spec01_scheds.append(spec01_sched)

qobj = assemble(spec01_scheds, backend=backend, **job_params)
spec01_job = backend.run(qobj)
print(spec01_job.result())

