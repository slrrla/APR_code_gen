from qiskit.transpiler import PassManager, StagedPassManager
from qiskit_nature.second_q.mappers import QubitConverter
from qiskit_nature.second_q.circuit.library.ansatzes import UCC
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.formats.molecule_info import MoleculeInfo
from qiskit_nature.second_q.mappers import ParityMapper

qubit_converter = QubitConverter(ParityMapper(), two_qubit_reduction=True, z2symmetry_reduction='auto')

molecule = MoleculeInfo(
    ["H", "Be", "H"],
    [(0., 0., -1.3264), (0., 0., 0.), (0., 0., 1.3264)],
)

driver = PySCFDriver.from_molecule(molecule, basis="sto3g")
electronic_structure_problem = driver.run()
second_quantized_hamiltonian = electronic_structure_problem.second_q_ops()

pauli_sum_operator = qubit_converter.convert(
    second_quantized_hamiltonian[0],
    num_particles=electronic_structure_problem.num_particles,
    sector_locator=electronic_structure_problem.symmetry_sector_locator
)

num_particles = electronic_structure_problem.num_particles
num_spatial_orbitals = electronic_structure_problem.num_spatial_orbitals

uccsdt_ansatz = UCC(
    num_spatial_orbitals,
    num_particles,
    excitations="sdt",
    qubit_converter=qubit_converter
)

# more info on pass managers here: https://qiskit.org/documentation/apidoc/transpiler.html
pm = StagedPassManager(stages=["init"])
circuit = pm.run(uccsdt_ansatz)
print(circuit.depth())
