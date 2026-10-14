# Reported bug: QiskitError when executing a circuit built from the
# qiskit_quantum_knn package - the transpiler cannot unroll a custom
# unitary-based gate ("cphi_0") to the requested basis.
from qiskit_quantum_knn.qknn.qknn_construction import (
    create_oracle,
    initialise_qknn,
    state_transformation,
    add_measurements,
)
from qiskit import BasicAer, execute

n_dim_qubits = 1    # must be log(len(test_state))
n_samps_qubits = 1  # must be log(len(train_data))

test_state = [0, 1]
train_data = [
    [1, 0],
    [0, 1],
]

oracle = create_oracle(train_data)
init_circ = initialise_qknn(n_dim_qubits, n_samps_qubits, test_state)
state_circ = state_transformation(init_circ, oracle)
final_circ = add_measurements(state_circ)

backend = BasicAer.get_backend('qasm_simulator')

# This raises:
# QiskitError: "Cannot unroll the circuit to the given basis,
# ['u1', 'u2', 'u3', 'cx', 'id', 'unitary']. Instruction cphi_0 not
# found in equivalence library and no rule found to expand."
job = execute(final_circ, backend, shots=1024)
