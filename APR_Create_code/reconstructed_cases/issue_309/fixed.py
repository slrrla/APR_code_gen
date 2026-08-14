from qiskit.opflow import I, X
from qiskit.opflow import PauliTrotterEvolution, Suzuki
from qiskit.circuit import Parameter
from numpy import sqrt

_const = 1 / (2 * sqrt(2))
A = _const * (I ^ X) + _const * (X ^ I)

phi = Parameter('ϕ')
evolution_op = (phi * A).exp_i()  # exp(-iϕA)

trotterized_op = PauliTrotterEvolution(trotter_mode=Suzuki(order=1)).convert(evolution_op)
circ = trotterized_op.to_circuit()
circ.draw('mpl')
