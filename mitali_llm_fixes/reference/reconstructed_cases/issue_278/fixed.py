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

# Fix: access the raw result of the eigensolver to retrieve the
# optimal variational parameters found by the VQE optimizer.
my_res = res.raw_result
# The dict of each parameter and its associated value
my_param_dict = res.raw_result.optimal_parameters
# The array of all the values
my_param_list = res.raw_result.optimal_point
print(my_param_dict)
print(my_param_list)
