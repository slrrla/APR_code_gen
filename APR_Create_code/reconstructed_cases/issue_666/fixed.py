from qiskit import QuantumCircuit
from qiskit.quantum_info import PauliList
from qiskit.aqua.operators import X, Y, Z, I, CircuitOp, CircuitStateFn

# The list of Pauli observables from the tutorial.
observables = PauliList(["ZZII", "IZZI", "IIZZ", "XIXI", "ZIZZ", "IXIX"])
print(observables)

# You can define your operator as a circuit
circuit = QuantumCircuit(2)
circuit.z(0)
circuit.z(1)
op = CircuitOp(circuit)  # and convert to an operator

# or if you have a WeightedPauliOperator, do
# op = weighted_pauli_op.to_opflow()

# but here we'll use the H2-molecule Hamiltonian
op = (-1.0523732 * I ^ I) + (0.39793742 * I ^ Z) + (-0.3979374 * Z ^ I) \
    + (-0.0112801 * Z ^ Z) + (0.18093119 * X ^ X)

# define the state w.r.t. which you want the expectation value
psi = QuantumCircuit(2)
psi.x(0)
psi.x(1)

# convert to a state
psi = CircuitStateFn(psi)

# easy expectation value, use for small systems only!
print('Math:', psi.adjoint().compose(op).compose(psi).eval().real)
