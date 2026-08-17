# Fix: list the backends actually available on the provider and pick one of those
# instead of hardcoding the retired 'ibmq_16_melbourne' backend.

from qiskit.providers.exceptions import QiskitBackendNotFoundError

class FakeIBMQProvider:
    def __init__(self):
        self._backends = ['ibmq_qasm_simulator', 'ibmq_manila', 'ibmq_lima']

    def backends(self):
        return list(self._backends)

    def get_backend(self, name):
        for b in self._backends:
            if b == name:
                return b
        raise QiskitBackendNotFoundError("No backend matches the criteria")


provider = FakeIBMQProvider()

# List all backends available on this provider
available = [p for p in provider.backends()]
print(available)

# Pick one that actually exists instead of the retired 'ibmq_16_melbourne'
qcomp = provider.get_backend(available[0])
