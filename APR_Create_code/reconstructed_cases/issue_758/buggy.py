import numpy as np
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.chemistry.drivers.molecule import Molecule
from qiskit.chemistry.core import Hamiltonian, TransformationType, QubitMappingType
from qiskit.aqua.algorithms import NumPyMinimumEigensolver

# Water molecule geometry given by the user (contains a typo: both
# hydrogens use the same sin() term for the y-coordinate, which makes
# the geometry nearly degenerate and crashes the PySCF driver / kernel).
angle = np.deg2rad(104.45 / 2)
dist = 0.9584
molecule = Molecule(
    geometry=[
        ['O', [0., 0., 0.]],
        ['H', [dist * np.sin(angle), -dist * np.cos(angle), 0.]],
        ['H', [-dist * np.sin(angle), -dist * np.sin(angle), 0.]],
    ],
    charge=0,
    multiplicity=1,
)

driver = PySCFDriver(molecule=molecule, unit=UnitsType.ANGSTROM, basis='sto6g')
qmolecule = driver.run()  # kernel dies here on the malformed geometry

ferOp = Hamiltonian(
    transformation=TransformationType.FULL,
    qubit_mapping=QubitMappingType.PARITY,
    two_qubit_reduction=True,
    freeze_core=True,
    orbital_reduction=[],
    z2symmetry_reduction='auto',
)
qubitOp, aux_ops = ferOp.run(qmolecule)

exact_result = NumPyMinimumEigensolver(qubitOp).run()
print(exact_result)
