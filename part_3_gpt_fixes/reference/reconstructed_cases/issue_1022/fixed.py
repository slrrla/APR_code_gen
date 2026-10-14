from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit import Aer, execute

qc2 = QuantumCircuit(2)
qc2.x(1)  # prepare the state |10>

two_qbit_QFT_ckt = QFT(2, do_swaps=False, inverse=True)  # here are the changes
qft_ckt_2 = qc2 + two_qbit_QFT_ckt
rev_qft_ckt_2 = qft_ckt_2.reverse_bits()  # same as putting swaps in the end of the circuit

# apply QFT on the state |10>
state_backend = Aer.get_backend('statevector_simulator')
qft_res_2 = execute(rev_qft_ckt_2, state_backend).result().get_statevector()
print(qft_res_2)
