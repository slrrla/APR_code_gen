import inspect
from qiskit_ibm_runtime import fake_provider

MIN_QUBITS = 14
MAX_ERROR = float('inf')
MIN_DEC_PLACE = 3

least_noisy_fakebackend = None
least_noisy_fakebackend_name = None
lowest_readout_error = MAX_ERROR

fb_list = [name for name, obj in inspect.getmembers(fake_provider)
           if inspect.isclass(obj) and name.startswith('Fake')]

def get_avg_readout_error(backend):
    try:
        nqubit = backend.configuration().n_qubits
        properties = backend.properties()
        tre = 0
        for qubit in range(nqubit):
            re = properties.qubit_property(qubit, 'readout_error')[0]
            tre += re
        return tre / nqubit
    except AttributeError:
        return MAX_ERROR

for backend_name in fb_list:
    try:
        backend_class = getattr(fake_provider, backend_name)
        backend = backend_class()
        # fake backend should have at least MIN_QUBITS qubits
        if backend.configuration().n_qubits < MIN_QUBITS:
            continue
        tmp = get_avg_readout_error(backend)
        readout_error_str = f"{tmp:.10f}"
        # ignore backend that doesn't have enough precision
        if len(readout_error_str.split('.')[1].rstrip('0')) < MIN_DEC_PLACE:
            continue
        avg_readout_error = tmp
        if avg_readout_error < lowest_readout_error:
            lowest_readout_error = avg_readout_error
            least_noisy_fakebackend_name = backend_name
            least_noisy_fakebackend = backend
    except Exception:
        continue

if least_noisy_fakebackend_name:
    print(f"Least noisy backend: {least_noisy_fakebackend_name}, "
          f"avg readout error: {lowest_readout_error}, "
          f"n_qubits: {least_noisy_fakebackend.configuration().n_qubits}")
else:
    print("No FakeBackend matched")
