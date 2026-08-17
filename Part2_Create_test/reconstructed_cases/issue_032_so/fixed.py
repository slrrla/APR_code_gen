from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer import QasmSimulator

# Create a quantum circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Get the Qasm simulator and set the backend options
aer_qasm_simulator = Aer.get_backend('qasm_simulator')

# Set the backend options, method set to statevector
options = {'method': 'statevector'}

# Execute circuit using the backend options created, memory and shots are execute params
job = execute(qc, aer_qasm_simulator, backend_options=options, memory=True, shots=10)
result = job.result()

# Pull the memory slots for the circuit
memory = result.get_memory(qc)

# Print the results from the memory slots
print('Memory results: ', memory)
