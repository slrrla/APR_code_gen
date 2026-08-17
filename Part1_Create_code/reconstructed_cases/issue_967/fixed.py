from qiskit.optimization import QuadraticProgram
from qiskit.optimization.converters import QuadraticProgramToQubo
import dimod

# Model a simple problem with Qiskit's QuadraticProgram
model = QuadraticProgram("Binary Test")
model.binary_var('x')
model.binary_var('y')
model.minimize(linear=[1, 2], quadratic={('x', 'y'): 3})

# Convert the QuadraticProgram into QUBO form, folding constraints
# into the objective and mapping integer variables to binary ones.
converter = QuadraticProgramToQubo()
qubo = converter.convert(model)

# Build a BQM directly from the QUBO objective coefficients
bqm_binary = dimod.as_bqm(
    qubo.objective.linear.to_array(),
    qubo.objective.quadratic.to_array(),
    dimod.BINARY,
)

# Sample locally instead of contacting a real D-Wave QPU
sampler = dimod.SimulatedAnnealingSampler()
result = sampler.sample(bqm_binary, num_reads=1024)
print(result)

# Alternative approach: the D-Wave Qiskit plugin exposes a
# MinimumEigenSolver-compatible interface (requires real QPU/network
# access, so it is left commented out here):
# from qiskit.optimization.algorithms import MinimumEigenOptimizer
# from dwave.plugins.qiskit import DWaveMinimumEigensolver
# dwave_solver = DWaveMinimumEigensolver()
# optimizer = MinimumEigenOptimizer(dwave_solver)
# result = optimizer.solve(model)
# print(result.min_eigen_solver_result.sampleset.to_pandas_dataframe())
