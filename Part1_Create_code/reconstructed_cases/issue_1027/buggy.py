import numpy as np
import pylab
import copy
from qiskit import BasicAer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import NumPyMinimumEigensolver, VQE
from qiskit.aqua.components.optimizers import SLSQP
from qiskit.chemistry.components.initial_states import HartreeFock
from qiskit.chemistry.components.variational_forms import UCCSD
from qiskit.chemistry.drivers import PySCFDriver
from qiskit.chemistry.algorithms.ground_state_solvers import GroundStateEigensolver
from qiskit.chemistry.algorithms.ground_state_solvers.minimum_eigensolver_factories import VQEUCCSDFactory
from qiskit.chemistry.transformations import (FermionicTransformation,
                                               FermionicTransformationType,
                                               FermionicQubitMappingType)

molecule = 'H .0 .0 -{0}; Li .0 .0 {0}'
distances = np.arange(0.5, 4.25, 0.25)
vqe_energies = []
hf_energies = []
exact_energies = []

for i, d in enumerate(distances):
    print('step', i)
    # set up the experiment
    driver = PySCFDriver(molecule.format(d / 2), basis='sto3g')

    fermionic_transformation = FermionicTransformation(
        transformation=FermionicTransformationType.FULL,
        qubit_mapping=FermionicQubitMappingType.JORDAN_WIGNER,
        two_qubit_reduction=False,
        freeze_core=False)

    qubit_op, aux_ops = fermionic_transformation.transform(driver)

    # VQE
    optimizer = SLSQP(maxiter=1000)
    initial_state = HartreeFock(
        fermionic_transformation.molecule_info['num_orbitals'],
        fermionic_transformation.molecule_info['num_particles'],
        qubit_mapping=fermionic_transformation.qubit_mapping,
        two_qubit_reduction=fermionic_transformation._two_qubit_reduction)

    # VQE: passing initial_state as initial_point is wrong -- it has no len()
    vqe_solver = VQEUCCSDFactory(
        QuantumInstance(BasicAer.get_backend('statevector_simulator')),
        optimizer, initial_state)

    calc = GroundStateEigensolver(fermionic_transformation, vqe_solver)
    res = calc.solve(driver)
    print(res)
