try:
    from qiskit_ibm_runtime.fake_provider import FakeOslo
    backend = FakeOslo()
    print(backend.qubit_properties(0))
    print(backend.qubit_properties(range(7)))
except ImportError:
    try:
        from qiskit.providers.fake_provider import FakeOslo
        backend = FakeOslo()
        print(backend.qubit_properties(0))
        print(backend.qubit_properties(range(7)))
    except (ImportError, AttributeError):
        print("FakeOslo not available in this version")
