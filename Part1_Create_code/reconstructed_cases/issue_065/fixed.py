from qiskit import BasicAer
from qiskit.utils import QuantumInstance
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit.circuit.library import TwoLocal
from qiskit_nature.drivers import PySCFDriver, UnitsType
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.mappers.second_quantization import JordanWignerMapper
from qiskit_nature.converters.second_quantization import QubitConverter

driver = PySCFDriver(atom='Li .0 .0 .0; H .0 .0 1.5049', unit=UnitsType.ANGSTROM, charge=0, spin=0, basis='sto3g')

# create second quantised operator
es_problem = ElectronicStructureProblem(driver)
seconded_quanitsied_oprator = es_problem.second_q_ops()
print(seconded_quanitsied_oprator)

# convert to qubit operator
qubit_transformation = QubitConverter(JordanWignerMapper())
qubit_operator = qubit_transformation.convert(seconded_quanitsied_oprator[0])
print(qubit_operator)

# set up simulator
backend = BasicAer.get_backend('statevector_simulator')
quantum_instance = QuantumInstance(backend=backend)

# VQE algorithm
groundstate_energies = []
classical_optimizer = SLSQP(maxiter=1000)

ansatz = TwoLocal(rotation_blocks='ry', entanglement_blocks='cz')

vqe = VQE(ansatz=ansatz,
          optimizer=SLSQP,
          quantum_instance=quantum_instance)
vqe_result = vqe.compute_minimum_eigenvalue(qubit_operator)
