from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.providers.aer.noise import NoiseModel
import collections

secret_number = "1010"
n = len(secret_number)

circuit = QuantumCircuit(n + 1, n)
circuit.h(range(n))
circuit.x(n)
circuit.h(n)
circuit.barrier()
for i, v in enumerate(reversed(secret_number)):
    if v == "1":
        circuit.cx(i, n)
circuit.barrier()
circuit.h(range(n))
circuit.barrier()
circuit.measure(range(n), range(n))

simulator = Aer.get_backend("qasm_simulator")
sim_result = execute(circuit, backend=simulator, shots=4096).result()

IBMQ.load_account()
provider = IBMQ.get_provider("ibm-q")
qcomp = provider.get_backend("ibmq_burlington")

noise_model = NoiseModel.from_backend(qcomp)
coupling_map = qcomp.configuration().coupling_map
basis_gates = noise_model.basis_gates
noisy_result = execute(
    circuit,
    simulator,
    coupling_map=coupling_map,
    basis_gates=basis_gates,
    noise_model=noise_model,
    shots=4096,
).result()
counts = noisy_result.get_counts(circuit)

c = collections.Counter(counts)
print("result simulation:")
print(sim_result.get_counts())
print("results (top 5):")
print(c.most_common(5))
