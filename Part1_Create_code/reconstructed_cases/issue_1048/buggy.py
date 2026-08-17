from qiskit.opflow import X, Y, Z, I, PauliTrotterEvolution
from qiskit.circuit import Parameter

hamiltonian = 3*(X^X^Z) - 1*(Z^X^Z)

# evolution operator
evo_time = Parameter('t')
evolution_op = (evo_time*hamiltonian).exp_i()
print(evolution_op)

# into circuit
num_time_slices = 1
trotterized_op = PauliTrotterEvolution(
    trotter_mode='trotter', reps=num_time_slices).convert(evolution_op)

# Bug: only the top-level circuit is drawn, so the individual gates
# inside the wrapped sub-blocks are not visible.
trotterized_op.to_circuit().draw('mpl')
