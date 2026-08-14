# Reproduces: QiskitBackendNotFoundError when requesting a retired backend
# (ibmq_16_melbourne was retired and is no longer available on the provider)

from qiskit.providers.exceptions import QiskitBackendNotFoundError

# Local stand-in for an IBMQ provider (no network / credentials involved)
class FakeIBMQProvider:
    def __init__(self):
        # only currently-active backends are listed here
        self._backends = ['ibmq_qasm_simulator', 'ibmq_manila', 'ibmq_lima']

    def backends(self):
        return list(self._backends)

    def get_backend(self, name):
        for b in self._backends:
            if b == name:
                return b
        raise QiskitBackendNotFoundError("No backend matches the criteria")


# Original user code (mirrors: IBMQ.load_account(); provider = IBMQ.get_provider('ibm-q'))
provider = FakeIBMQProvider()
qcomp = provider.get_backend('ibmq_16_melbourne')  # BUG: this backend has been retired
