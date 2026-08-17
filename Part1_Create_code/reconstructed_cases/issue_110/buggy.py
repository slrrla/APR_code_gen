import numpy as np
from qiskit.chemistry.components.variational_forms import UCCSD
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.chemistry import FermionicOperator
from qiskit.aqua import QuantumInstance

def get_qubit_op(atom, basis, map_type):
    driver = PySCFDriver(atom=atom, unit=UnitsType.ANGSTROM, charge=0, spin=0, basis=basis)
    molecule = driver.run()
    repulsion_energy = molecule.nuclear_repulsion_energy
    num_particles = molecule.num_alpha + molecule.num_beta
    num_spin_orbitals = molecule.num_orbitals * 2
    ferOp = FermionicOperator(h1=molecule.one_body_integrals, h2=molecule.two_body_integrals)
    qubitOp = ferOp.mapping(map_type=map_type, threshold=0.00000001)
    # qubitOp = Z2Symmetries.two_qubit_reduction(qubitOp, num_particles)
    shift = repulsion_energy
    return qubitOp, num_particles, num_spin_orbitals, shift

atom = 'H .0 .0 .0; H .0 .0 0.74'
qubitOp, num_particles, num_spin_orbitals, shift = get_qubit_op(atom, basis='sto3g', map_type='parity')
num_qubits = qubitOp.num_qubits
print('num_qubits = ', num_qubits)

from qiskit.chemistry.components.initial_states import HartreeFock
init_state = HartreeFock(num_spin_orbitals, num_particles, 'parity', two_qubit_reduction=False)

# setup the variational form for VQE
from qiskit.chemistry.components.variational_forms import UCCSD
var_form_vqe = UCCSD(
    num_orbitals=num_spin_orbitals,
    num_particles=num_particles,
    initial_state=init_state,
    qubit_mapping='parity',
    two_qubit_reduction=False
)

print('var_form_vqe.num_parameters = ', var_form_vqe.num_parameters)
var_form_vqe.construct_circuit([1, 1, 1]).draw()
# Give some random parameters and draw the circuit at the "Evolution" block level
