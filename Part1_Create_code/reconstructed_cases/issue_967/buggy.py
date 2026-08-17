from qiskit.optimization import QuadraticProgram
import dimod

# Model a simple problem with Qiskit's QuadraticProgram
model = QuadraticProgram("Binary Test")
model.binary_var('x')
model.binary_var('y')
model.minimize(linear=[1, 2], quadratic={('x', 'y'): 3})

# Attempt to directly turn a QuadraticProgram into a D-Wave BQM.
# There is no such direct conversion supported by dimod/qiskit-optimization.
bqm = dimod.AdjVectorBQM(model)
