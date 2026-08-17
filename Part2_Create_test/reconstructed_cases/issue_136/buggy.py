# Old-style IBMQ authentication flow (deprecated / now fails with 403 Forbidden)
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QiskitError
from qiskit import execute, IBMQ

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

    # Old account management calls that now raise HTTPError 403 Forbidden
    IBMQ.delete_account()
    IBMQ.active_account()
    IBMQ.save_account('myAPI toke ')
    IBMQ.save_account('my API toke')
    IBMQ.load_account()

    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibmq_qasm_simulator')

    job_exp = execute(qc, backend, shots=2048)
    result_exp = job_exp.result()

    print('Counts: ', result_exp.get_counts(qc))
except QiskitError as ex:
    print('There was an error in the circuit!. Error = {}'.format(ex))
