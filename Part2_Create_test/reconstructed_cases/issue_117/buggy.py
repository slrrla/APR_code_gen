import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
# missing circ.save_statevector() call, so no statevector data is saved

backend = AerSimulator(method='statevector')
backend.set_options(
    max_parallel_threads=0,
    max_parallel_experiments=0,
    max_parallel_shots=1,
    statevector_parallel_threshold=16
)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
qc_combine = pm.run(circ)
result = backend.run(qc_combine, shots=1)
psi_out_complex = result.result()
print(psi_out_complex)
