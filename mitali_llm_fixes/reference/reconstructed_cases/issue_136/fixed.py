# This code works with qiskit 0.41.0
# Import Qiskit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QiskitError
from qiskit import execute
from qiskit_ibm_provider import IBMProvider
from qiskit_ibm_provider import least_busy

try:
    # Create a Quantum Register with 2 qubits.
    q = QuantumRegister(2)
    # Create a Classical Register with 2 bits.
    c = ClassicalRegister(2)
    # Create a Quantum Circuit
    qc = QuantumCircuit(q, c)
    vector = [0.5, 0.5, 0.5, 0.5]
    qc.initialize(vector)
    qc.draw()
    # Add a Measure gate to see the state.
    qc.measure(q, c)

    # the following instruction must be used the very first time, then commented
    # IBMProvider.save_account(token='MY_API_TOKEN')
    # the following instruction is the one you will use always
    provider = IBMProvider()

    # display current supported backends
    print(provider.backends(min_num_qubits=5, simulator=False, operational=True))
    small_devices = provider.backends(min_num_qubits=5, simulator=False, operational=True)
    backend = least_busy(small_devices)
    print(backend)

    # running the job
    job_exp = execute(qc, backend, shots=2048)
    result_exp = job_exp.result()

    # Show the results
    print('Counts: ', result_exp.get_counts(qc))
except QiskitError as ex:
    print('There was an error in the circuit!. Error = {}'.format(ex))
