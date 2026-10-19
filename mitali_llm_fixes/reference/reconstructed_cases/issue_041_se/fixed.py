import qiskit
from qiskit import Aer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QPE
from qiskit.aqua.operators import WeightedPauliOperator
from qiskit.aqua.components.initial_states import Custom
from qiskit.circuit.library import QFT

print(qiskit.__qiskit_version__)

a = Custom(1, state='uniform')  # Initial state as intended

dict = {
    'paulis': [{"coeff": {"imag": 0.00, "real": 1}, "label": "X"}]
}
b = WeightedPauliOperator.from_dict(dict)  # Operator for input into QPE

# -------- Setting up Backend --------#
quantum_instance = QuantumInstance(backend=Aer.get_backend("statevector_simulator"), shots=1)
# ------------------------------------#

n_ancillae = 3
iqft = QFT(n_ancillae).inverse()
qpe = QPE(b, a, iqft, num_time_slices=1, num_ancillae=n_ancillae,
          expansion_mode='trotter', expansion_order=1, shallow_circuit_concat=False)
qpe_result = qpe.run(quantum_instance)
qc = qpe.construct_circuit(measurement=True)
qc.draw()
