from qiskit_nature.drivers import PySCFDriver
from qiskit_nature.transformers import ActiveSpaceTransformer

# H2O molecule setup with sto-3g basis set
driver = PySCFDriver(atom="O 0 0 0; H 0 0 0.96; H 0.93 0 -0.24",
                      basis="sto-3g")

# Trying to select an active space, but not specifying which
# molecular orbitals should be active -- only giving counts.
# This does not let us exclude the 3a1 & 1b1 orbitals explicitly.
transformer = ActiveSpaceTransformer(4, 4)

molecule = driver.run()
active_molecule = transformer.transform(molecule)
