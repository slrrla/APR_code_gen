# Minimal reconstruction of a VQC training run that hits IBM Q backend
# status errors (520 Server Error) while polling job status on the
# real "ibmq_16_melbourne" hardware backend.
#
# NOTE: per dataset policy we never contact a real backend here, so a
# local simulator stands in for the hardware device the asker used.
from qiskit import Aer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import VQC
from qiskit.aqua.components.optimizers import SPSA
from qiskit.aqua.components.feature_maps import SecondOrderExpansion
from qiskit.aqua.components.variational_forms import RYRZ

feature_dim = 2

featuremap = SecondOrderExpansion(feature_dimension=feature_dim, depth=2)
var_form = RYRZ(num_qubits=feature_dim, depth=3)
optimizer = SPSA(max_trials=100)

# The asker ran against the real "ibmq_16_melbourne" device, which was
# offline for upgrades, causing repeated 520 Server Errors when the
# job status/backend status was polled during training.
backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1024)

df_train_test_x_Q = [[0.1, 0.2], [0.3, 0.4]]
df_train_test_y_Q = {'A': [0], 'B': [1]}

def QSVMsetup(featuremap):
    svm = VQC(optimizer, featuremap, var_form, df_train_test_x_Q, df_train_test_y_Q)
    training_result = svm.train(df_train_test_x_Q, df_train_test_y_Q, quantum_instance)
    return training_result

QSVMsetup(featuremap)
