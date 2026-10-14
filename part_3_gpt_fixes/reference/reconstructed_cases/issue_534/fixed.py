# Fix: cleanly reinstall qiskit-nature with the pyscf extra and pyscf itself,
# then re-run the exact same ground state solver code.

import os

os.system("pip uninstall qiskit_nature --yes")
os.system("pip uninstall pyscf --yes")
os.system("pip show qiskit_nature")
os.system("pip show pyscf")
os.system("pip install qiskit-nature[pyscf] -U")
os.system("pip install qiskit-nature")
os.system("pip install pyscf")

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

res = calc.solve(es_problem)
print(res)
