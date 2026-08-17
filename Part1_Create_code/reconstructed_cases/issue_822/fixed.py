# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, execute, Aer, QuantumRegister, ClassicalRegister
from qiskit.compiler import transpile, assemble

def create_controled_gate():
    h_circuit = QuantumCircuit(1, name='H')
    h_circuit.h(0)
    gate = h_circuit.to_gate().control()
    return gate

circuit = QuantumCircuit(2)
controlled_gate = create_controled_gate()
circuit.append(controlled_gate, [0, 1])
cr = ClassicalRegister(2, 'creg')
circuit.add_register(cr)
circuit.measure(range(2), range(2))
circuit.draw()

aer_sim = Aer.get_backend('aer_simulator')

# Transpile the circuit into the simulator's supported basis gates
# before running it (cH is not a basis gate for the statevector method)
circuit = transpile(circuit, backend=aer_sim)
job = aer_sim.run(circuit, shots=1000)
hist = job.result().get_counts()
print(hist)
