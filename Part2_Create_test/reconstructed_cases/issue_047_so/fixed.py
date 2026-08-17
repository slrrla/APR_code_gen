# Upgrade qiskit-nature to >=0.5.0 (and use Python >=3.7) to get the
# "units" submodule and the "second_q" namespace.
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver

driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM,
)
