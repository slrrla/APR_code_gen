from qiskit.primitives import Estimator
from qiskit.providers.aer import QasmSimulator, AerSimulator
from qiskit.algorithms.optimizers import SLSQP
from qiskit.utils import QuantumInstance
from qiskit_nature.second_q.algorithms import NumPyMinimumEigensolverFactory
from qiskit_nature.second_q.algorithms.initial_points import HFInitialPoint
from qiskit_nature.second_q.algorithms.ground_state_solvers import GroundStateEigensolver, VQEUCCFactory
from qiskit_nature.second_q.formats.molecule_info import MoleculeInfo
from qiskit_nature.second_q.mappers import QubitConverter, ParityMapper
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import FreezeCoreTransformer
from qiskit_nature.second_q.circuit.library.ansatzes import UCC

objective_function_tolerance = 1e-6
slsqp = SLSQP(maxiter=10000, tol=objective_function_tolerance)
numpy_solver = NumPyMinimumEigensolverFactory()
quantum_instance = QuantumInstance(AerSimulator(method='statevector', device="CPU"))

molecule = MoleculeInfo(["Li", "H"], [(0.0, 0.0, 0.0), (0.0, 0.0, 1.595)])
driver = PySCFDriver.from_molecule(molecule, basis="sto3g")
electronic_structure_problem = driver.run()

transformer = FreezeCoreTransformer()
electronic_structure_problem = transformer.transform(electronic_structure_problem)

num_particles = electronic_structure_problem.num_particles
num_spatial_orbitals = electronic_structure_problem.num_spatial_orbitals
uccsd = UCC(num_spatial_orbitals, num_particles, excitations='sd')

def callback(eval_count, parameters, mean, std):
    print(eval_count)

vqe_factory = VQEUCCFactory(Estimator(), uccsd, slsqp, initial_point=HFInitialPoint())
vqe_factory.minimum_eigensolver.callback = callback

# ParityMapper is now imported, fixing the NameError.
converter = QubitConverter(ParityMapper(), two_qubit_reduction=True, z2symmetry_reduction=None)

gse = GroundStateEigensolver(converter, vqe_factory)
result = gse.solve(electronic_structure_problem)
print("function evaluations: ", result.raw_result.cost_function_evals)
