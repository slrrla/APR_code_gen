import numpy as np
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.chemistry.core import Hamiltonian, TransformationType, QubitMappingType
from qiskit.aqua.algorithms import NumPyMinimumEigensolver

# Because of the symmetry of the water molecule, use the Z-Matrix
# representation instead of the ambiguous/degenerate XYZ geometry.
atom_structure = "H; O 1 0.958; H 2 0.958 1 104.47"

driver = PySCFDriver(
    atom=atom_structure,
    unit=UnitsType.ANGSTROM,
    charge=0,
    spin=0,
    basis='sto6g',
)
qmolecule = driver.run()

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
