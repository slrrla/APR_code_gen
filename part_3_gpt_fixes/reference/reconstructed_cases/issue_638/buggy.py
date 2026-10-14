# User attempts to use the deprecated qiskit.chemistry FermionicOperator API
from qiskit.chemistry import FermionicOperator
from qiskit.chemistry.drivers import PySCFDriver, UnitsType

driver = PySCFDriver(atom='H .0 .0 .0; H .0 .0 .735', unit=UnitsType.ANGSTROM, basis='sto3g')
molecule = driver.run()

h1 = molecule.one_body_integrals
h2 = molecule.two_body_integrals

fer_op = FermiOpetator(h1=h1, h2=h2)
qubit_op = fer_op.mapping(map_type='jordan_wigner')
print(qubit_op)
