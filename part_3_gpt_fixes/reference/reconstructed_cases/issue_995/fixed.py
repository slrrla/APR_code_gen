from qiskit import IBMQ
from qiskit.providers.aer.noise import NoiseModel, ReadoutError

provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_quito')

# Build the noise model directly from a real (or fake) backend
nm_1 = NoiseModel.from_backend(backend)

print('The readout errors defined before altering are:')
print(nm_1._local_readout_errors)

# Customize the noise model using its attributes/methods instead of
# the deprecated to_dict()/from_dict() approach
q0_RO_er = ReadoutError([[0.8, 0.2], [0.2, 0.8]])
nm_1._local_readout_errors[(0,)] = q0_RO_er

print()
print('The readout errors after altering are:')
print(nm_1._local_readout_errors)
