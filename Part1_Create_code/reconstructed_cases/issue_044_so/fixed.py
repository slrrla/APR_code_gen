from qiskit import pulse
from qiskit.compiler import assemble
from qiskit.providers.fake_provider import FakeProvider

# Instead of hardcoding a backend, filter for ones that actually support OpenPulse
provider = FakeProvider()
backends_supporting_openpulse = provider.backends(filters=lambda b: b.configuration().open_pulse)
backend = backends_supporting_openpulse[0]

with pulse.build(backend) as sched:
    pulse.play(pulse.Gaussian(duration=160, amp=0.1, sigma=40), pulse.DriveChannel(0))

frequency_sweep_program = assemble(sched, backend=backend, meas_level=1, meas_return='avg', shots=256)

job = backend.run(frequency_sweep_program)
frequency_sweep_results = job.result(timeout=120)  # timeout parameter set to 120 seconds
