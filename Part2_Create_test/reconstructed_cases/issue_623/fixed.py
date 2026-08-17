from qiskit import QuantumCircuit, QuantumRegister
from qiskit import schedule
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

backend = FakeBrisbane()
properties = backend.qubit_properties(range(backend.num_qubits))

qr = QuantumRegister(1)
qc = QuantumCircuit(qr)
qc.sx(0)
qc.measure_all()

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_qc = pm.run(qc)

scheduled_circuit = schedule(isa_qc, backend=backend)
circuit_duration = scheduled_circuit.duration * backend.configuration().dt

print("execution time {:}[ns]".format(circuit_duration * 1000 * 1000 * 1000))
print("t1 {:}[ns]".format(properties[0].t1 * 1000 * 1000 * 1000))
print("t2 {:}[ns]".format(properties[0].t2 * 1000 * 1000 * 1000))
