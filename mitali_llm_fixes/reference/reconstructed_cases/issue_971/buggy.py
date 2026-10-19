from qiskit import transpile
from qiskit.transpiler import PassManager, StagedPassManager
from qiskit.providers.fake_provider import FakeWashington
from qiskit_nature.converters.second_quantization import QubitConverter
# from qiskit_nature.second_q.mappers import QubitConverter (same result)
from qiskit_nature.second_q.circuit.library.ansatzes import UCC, UCCSD
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.formats.molecule_info import MoleculeInfo
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.second_q.transformers import FreezeCoreTransformer

qubit_converter = QubitConverter(ParityMapper(), two_qubit_reduction=True, z2symmetry_reduction='auto')

molecule = MoleculeInfo(["Li", "H"], [(0.0, 0.0, 0.0), (0.0, 0.0, 1.595)])
driver = PySCFDriver.from_molecule(molecule, basis="sto3g")
transformer = FreezeCoreTransformer()
electronic_structure_problem = transformer.transform(driver.run())
second_quantized_hamiltonian = electronic_structure_problem.second_q_ops()

pauli_sum_operator = qubit_converter.convert(second_quantized_hamiltonian[0], num_particles=electronic_structure_problem.num_particles)

num_particles = electronic_structure_problem.num_particles
num_spatial_orbitals = electronic_structure_problem.num_spatial_orbitals
num_spin_orbitals = electronic_structure_problem.num_spin_orbitals

ucc_ansatz = UCC(num_spatial_orbitals, num_particles, excitations='sd', qubit_converter=qubit_converter, alpha_spin=True, beta_spin=True, max_spin_excitation=1, generalized=True, preserve_spin=True, reps=5)

decomposed_circuit = ucc_ansatz.decompose().decompose().decompose()
print("depth: ", decomposed_circuit.depth())

transpiled_circuit = transpile(ucc_ansatz, FakeWashington(), optimization_level=3)
print("depth transpiled: ", transpiled_circuit.depth())
print(dict(transpiled_circuit.count_ops()))
print("ansatz parameters: ", len(ucc_ansatz.parameters.data))
