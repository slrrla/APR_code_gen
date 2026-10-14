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
qobj = assemble(circuit, shots=1000)
job = aer_sim.run(qobj)
hist = job.result().get_counts()
print(hist)
