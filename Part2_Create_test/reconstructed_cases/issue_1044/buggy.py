# Reproduces: ModuleNotFoundError: No module named 'qiskit.providers.basebackend'
# caused by installing a newer qiskit-terra that removed BaseBackend,
# which qiskit_rng (last released Jan 2021) still imports internally.

from qiskit_rng import Generator   # fails at import time on modern qiskit-terra
from qiskit import IBMQ

IBMQ.load_account()
rng_provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend = rng_provider.backends.ibmq_manila

generator = Generator(backend=backend)
output = generator.sample(num_raw_bits=20001).block_until_ready()
qiskit_raw = output.raw_bits
print(qiskit_raw)
