# Fix: pin compatible dependency versions before running:
#   pip install "qiskit-terra==0.16.2"
#   pip install "qiskit-ibmq-provider~=0.10"
# With those versions, qiskit.providers.basebackend still exists and
# qiskit_rng imports successfully.
#
# A local simulator is used here instead of a real IBMQ backend to
# avoid any network/hardware access.

from qiskit_rng import Generator
from qiskit import Aer

backend = Aer.get_backend('qasm_simulator')

generator = Generator(backend=backend)
output = generator.sample(num_raw_bits=20001).block_until_ready()
qiskit_raw = output.raw_bits
print(qiskit_raw)
