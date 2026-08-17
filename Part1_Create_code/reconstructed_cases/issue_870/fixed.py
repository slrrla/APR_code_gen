# Essential Imports
import numpy as np

# Qiskit Imports
from qiskit.providers.aer import PulseSimulator
from qiskit.providers.aer.pulse import PulseSystemModel
from qiskit import assemble
from qiskit.tools.monitor import job_monitor
from qiskit.test.mock import FakeArmonk  # local stand-in for the real ibmq_armonk backend
import qiskit.pulse as pulse

backend = FakeArmonk()

# Instead of building the simulator directly from the backend, build a
# PulseSystemModel from the backend and use a plain PulseSimulator, passing
# the system model to run(). This avoids "Job Status: job incurred error".
armonk_model = PulseSystemModel.from_backend(backend)
backend_pulse_simulator = PulseSimulator()

# Get information about the backend
qubit = 0
backend_defaults = backend.defaults()
backend_properties = backend.properties()
qubit_frequency_updated = backend_properties.qubit_property(qubit, 'frequency')[0]
inst_sched_map = backend_defaults.instruction_schedule_map
measure_schedule = inst_sched_map.get('measure', qubits=[qubit])

# Assemble a job - circuit with a single qubit -> u2 gate -> measurement
num_shots_per_point = 1024
drive_chan = pulse.DriveChannel(qubit)
schedule = pulse.Schedule()
schedule += inst_sched_map.get('u2', [qubit], P0=0.0, P1=np.pi)  # Removing this solves the issue - why?
schedule += measure_schedule << schedule.duration

pulse_program = assemble(
    schedule,
    backend=backend_pulse_simulator,
    meas_level=2,
    meas_return="single",
    shots=num_shots_per_point,
    schedule_los=[{drive_chan: qubit_frequency_updated}]
)

# Run the job, passing the system model built from the backend
job = backend_pulse_simulator.run(pulse_program, armonk_model)
job_monitor(job)
