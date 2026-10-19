from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit import Aer, execute

qc2 = QuantumCircuit(2)
qc2.x(1)  # prepare the state |10>

two_qbit_QFT_ckt = QFT(2)
qft_ckt_2 = qc2 + two_qbit_QFT_ckt  # apply QFT on the state |10>

state_backend = Aer.get_backend('statevector_simulator')
qft_res_2 = execute(qft_ckt_2, state_backend).result().get_statevector()
print(qft_res_2)
