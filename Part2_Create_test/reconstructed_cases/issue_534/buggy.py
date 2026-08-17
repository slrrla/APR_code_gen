# Reproduces the "PySCF library is required to use 'PySCFDriver'" error
# from the Qiskit Nature ground-state-solvers tutorial.
# This assumes PySCF is not (properly) installed in the environment.

from qiskit_nature.drivers import Molecule
from qiskit_nature.drivers.second_quantization import PySCFDriver
from qiskit_nature.problems.second_quantization.electronic import ElectronicStructureProblem
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import JordanWignerMapper
from qiskit_nature.algorithms.ground_state_solvers import GroundStateEigensolver
from qiskit.algorithms import NumPyMinimumEigensolver

molecule = Molecule(
    geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]],
    charge=0,
    multiplicity=1,
)

driver = PySCFDriver(molecule=molecule)
es_problem = ElectronicStructureProblem(driver)

qubit_converter = QubitConverter(JordanWignerMapper())
solver = NumPyMinimumEigensolver()
calc = GroundStateEigensolver(qubit_converter, solver)

# This raises:
# MissingOptionalLibraryError: The 'PySCF' library is required to use 'PySCFDriver'.
res = calc.solve(es_problem)
print(res)
