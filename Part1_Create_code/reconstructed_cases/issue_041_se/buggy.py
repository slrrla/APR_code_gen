import numpy as np
from qiskit import QuantumCircuit, Aer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QPE
from qiskit.aqua.operators import MatrixOperator
from qiskit.aqua.components.initial_states import Custom
from qiskit.quantum_info import Statevector

# Prepare the |+> state
circ = QuantumCircuit(1)
circ.h(0)
a = Custom(num_qubits=1, state='zero', state_vector=None, circuit=circ)
blah = a.construct_circuit(mode='circuit', register=None)
statevec = Statevector.from_instruction(circ).data  # raw numpy array, not an initial-state object

# Operator for X
b = MatrixOperator(np.array([[0, 1], [1, 0]]), basis=None, z2_symmetries=None, atol=1e-12, name=None)

backend = Aer.get_backend('statevector_simulator')
qpe = QPE(operator=b, state_in=statevec, iqft=None, num_time_slices=1, num_ancillae=1,
          expansion_mode='trotter', expansion_order=1, shallow_circuit_concat=False)
quantum_instance = QuantumInstance(backend=backend)
results = qpe.run(quantum_instance)
