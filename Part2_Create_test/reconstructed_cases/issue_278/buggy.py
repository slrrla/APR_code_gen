import numpy as np
import pylab
import copy
from qiskit import BasicAer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import NumPyMinimumEigensolver, VQE
from qiskit.aqua.components.optimizers import SLSQP
from qiskit.chemistry.components.initial_states import HartreeFock
from qiskit.chemistry.components.variational_forms import UCCSD
from qiskit.chemistry.drivers import PySCFDriver, UnitsType, Molecule
from qiskit.chemistry.algorithms.ground_state_solvers import GroundStateEigensolver
from qiskit.chemistry.algorithms.ground_state_solvers.minimum_eigensolver_factories import VQEUCCSDFactory
from qiskit.chemistry.transformations import (FermionicTransformation, FermionicTransformationType, FermionicQubitMappingType)

molecule = Molecule(geometry=[['H', [0., 0., 0.]], ['H', [0., 0., 0.735]]], charge=0, multiplicity=1)
driver = PySCFDriver(molecule=molecule, unit=UnitsType.ANGSTROM, basis='sto3g')
transformation = FermionicTransformation(qubit_mapping=FermionicQubitMappingType.JORDAN_WIGNER)
vqe_solver = VQEUCCSDFactory(QuantumInstance(BasicAer.get_backend('statevector_simulator')))
calc = GroundStateEigensolver(transformation, vqe_solver)
res = calc.solve(driver)
print(res)

# Bug: the user only prints the final summary result and has no way to
# access the raw optimal variational parameters of the ansatz.
