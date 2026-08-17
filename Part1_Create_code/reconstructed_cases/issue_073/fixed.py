from qiskit_braket_provider import AWSBraketProvider
from braket.jobs import hybrid_job
from braket.aws import AwsDevice
from braket.devices import Devices
from qiskit import QuantumCircuit, QuantumRegister, transpile

def create_grover_oracle(target, num_qubits):
    qr = QuantumRegister(num_qubits)
    oracle_circuit = QuantumCircuit(qr)
    # to encode the target into the quantum state
    for i, bit in enumerate(address):  # NOTE: 'address' is undefined (not part of this fix)
        if bit == '1':
            oracle_circuit.x(i)
    # apply CZ gates pairwise between adjacent qubits
    for i in range(num_qubits - 1):
        oracle_circuit.cz(i, i+1)
    # uncompute the encoding
    for i, bit in enumerate(target):
        if bit == '1':
            oracle_circuit.x(i)
    return oracle_circuit

def create_diffusion_circuit(num_qubits):
    qr = QuantumRegister(num_qubits)
    diffusion_circuit = QuantumCircuit(qr)
    # apply Hadamard gates to all qubits
    diffusion_circuit.h(range(num_qubits))
    # apply X gate to all qubits
    diffusion_circuit.x(range(num_qubits))
    # apply multi-controlled Z gate
    diffusion_circuit.h(num_qubits-1)
    diffusion_circuit.mct(list(range(num_qubits-1)), num_qubits-1)
    diffusion_circuit.h(num_qubits-1)
    # apply X gate again
    diffusion_circuit.x(range(num_qubits))
    # apply Hadamard gates again
    diffusion_circuit.h(range(num_qubits))
    return diffusion_circuit

# @hybrid_job(device=AwsDevice(Devices.Amazon.TN1).arn)
def execute_quantum_circuit(circuit, shots=1000):
    backend = AWSBraketProvider().get_backend("TN1")
    transpiled_circuit = transpile(circuit, backend)
    job = backend.run(transpiled_circuit, shots=shots)
    # Get the result of the job
    result = job.result()
    # Get the counts of measurement outcomes
    counts = result.get_counts()
    return counts

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)

execute_quantum_circuit(circuit)
# {'11': 507, '00': 493}
