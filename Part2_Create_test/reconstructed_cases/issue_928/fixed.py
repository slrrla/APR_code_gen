from qiskit import IBMQ

# Load account and get a provider (as the user already had working)
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')

job_id = 'job_id_placeholder'

retrieve_job = provider.backend.retrieve_job(job_id)

# Use properties() to get a BackendProperties snapshot taken at the
# time the job was run - this is where gate errors and other
# configuration details live.
properties = retrieve_job.properties()
print(properties)

# Get a specific qubit property, e.g. T1/T2/readout_error for qubit 0
print(properties.qubit_property(0))

# Get the gate error for a specific gate/qubits, e.g. cx on qubits [0, 1]
print(properties.gate_error('cx', [0, 1]))

# Get a full dictionary representation of the BackendProperties
print(properties.to_dict())
