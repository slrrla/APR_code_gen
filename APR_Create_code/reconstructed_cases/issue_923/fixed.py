# required imports
from docplex.mp.model import Model
from qiskit.optimization.problems import QuadraticProgram
from qiskit.optimization.converters import QuadraticProgramToIsing

# specify problem
n = 3
a = 1.0
k = 2
t = range(1, n+1)

# build model with docplex
mdl = Model()
x = [mdl.binary_var() for i in range(n)]
objective = a*(k - mdl.sum(t[i]*x[i] for i in range(n)))**2
mdl.minimize(objective)

# convert to Qiskit's quadratic program
qp = QuadraticProgram()
qp.from_docplex(mdl)

# convert to Ising Hamiltonian
qp2ising = QuadraticProgramToIsing()
H, offset = qp2ising.encode(qp)

print('Offset:', offset)
print('Ising Hamiltonian:')
print(H.print_details())
