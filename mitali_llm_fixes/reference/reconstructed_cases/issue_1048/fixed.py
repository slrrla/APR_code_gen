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

# Fix: decompose the circuit to reveal the gates inside the sub-blocks.
circuit = trotterized_op.to_circuit()
decomposed = circuit.decompose()
decomposed.draw('mpl')
