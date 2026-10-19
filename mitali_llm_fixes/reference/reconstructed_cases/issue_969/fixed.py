from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.circuit.library import ZGate, XGate, RZGate, RYGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler
import numpy as np
from qiskit.circuit import ControlledGate

# FIX: use the built-in .control() helper which builds a correctly-sized
# controlled gate definition, avoiding the qubit-count mismatch.
cry = RYGate(np.pi / 2).control(3, ctrl_state='000')

qc = QuantumCircuit(4)
qc.append(cry, [0, 1, 2, 3])
qc.measure_all()

backend = AerSimulator()
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
shots = 1024
qc.draw()
isa_qc = pm.run(qc)

sampler = Sampler(mode=backend)
result = sampler.run([isa_qc], shots=shots).result()
pub_result = result[0]
counts = pub_result.data.meas.get_counts()
print(counts)
