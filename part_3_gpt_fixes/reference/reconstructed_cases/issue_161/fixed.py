import qiskit
print(qiskit.__qiskit_version__)
# >> {'qiskit-terra': '0.21.2', 'qiskit-aer': '0.10.4', 'qiskit-ignis': None,
#     'qiskit-ibmq-provider': '0.19.2', 'qiskit': '0.37.2', 'qiskit-nature': None,
#     'qiskit-finance': None, 'qiskit-optimization': None,
#     'qiskit-machine-learning': None}
#
# qiskit-terra: the "core" of qiskit, containing the circuit class, gates, etc.
# qiskit-aer: circuit simulators to test out your circuit.
# qiskit-ignis: noise modeling, error channels, quantum information and
#               error-correction utilities (superseded by qiskit-experiments).
# qiskit-ibmq-provider: running on the IBM cloud, QPUs or hosted simulators.
# qiskit: packages everything together.
# qiskit-nature, qiskit-finance, qiskit-optimization, qiskit-machine-learning:
#               tools to express problems in their respective domains as
#               quantum programs.
