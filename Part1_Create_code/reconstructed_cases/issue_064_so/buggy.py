from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver

driver = PySCFDriver(atom="H 0 0 0; H 0 0 0.735", basis="sto-3g")

es_problem = driver.run()

from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitConverter

converter = QubitConverter(JordanWignerMapper())

from qiskit.algorithms.optimizers import SLSQP
from qiskit_nature.second_q.algorithms import VQEUCCFactory
from qiskit_nature.second_q.circuit.library import UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

from qiskit_aer.primitives import Estimator as AerEstimator

seed = 170

# Buggy: using shots-based sampling (default) causes shot noise that,
# combined with the gradient-based SLSQP optimizer, gives wildly wrong results.
noiseless_estimator = AerEstimator(
    run_options={"seed": seed, "shots": 1024},
    transpile_options={"seed_transpiler": seed},
)

vqe_solver2 = VQEUCCFactory(noiseless_estimator, UCCSD(), SLSQP())
calc2 = GroundStateEigensolver(converter, vqe_solver2)
res2 = calc2.solve(es_problem)
print(res2)
