# The answer discusses several ansatz circuits available in Qiskit and when to use them:
# EfficientSU2 (real+complex amplitudes, hardware efficient),
# RealAmplitudes (real amplitudes only, hardware efficient),
# ExcitationPreserving (particle-number preserving, used e.g. for molecular problems).
from qiskit.circuit.library import EfficientSU2, RealAmplitudes, ExcitationPreserving

ansatz_efficient_su2 = EfficientSU2(num_qubits=4)
print(ansatz_efficient_su2)

ansatz_real_amplitudes = RealAmplitudes(num_qubits=4)
print(ansatz_real_amplitudes)

ansatz_excitation_preserving = ExcitationPreserving(num_qubits=4)
print(ansatz_excitation_preserving)
