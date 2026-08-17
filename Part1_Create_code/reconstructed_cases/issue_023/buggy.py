import numpy as np
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.circuit.library import RealAmplitudes

noQBits = 3
linear_dim = 2**noQBits
ansatz = RealAmplitudes(noQBits, reps=1, entanglement='full', insert_barriers=True)
psiTime0 = [0]*(linear_dim)
psiTime0[2] = 1
psiTime0 = Statevector(psiTime0,)
aer_sim = AerSimulator()
pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
gateEvolver = ansatz.assign_parameters(np.zeros(ansatz.num_parameters))
psiTest0 = psiTime0.evolve(gateEvolver)
prob0 = psiTime0.probabilities_dict()
probTest0 = psiTest0.probabilities_dict()
print(prob0)
print(probTest0)
