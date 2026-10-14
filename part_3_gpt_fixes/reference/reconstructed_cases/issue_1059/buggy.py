from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.compiler import transpile
from qiskit.providers.ibmq.managed import IBMQJobManager
from qiskit import Aer

backend = Aer.get_backend('qasm_simulator')

qrz = QuantumRegister(2)
crz = ClassicalRegister(2)

def qc(Variable):
    var_form = QuantumCircuit(2, 2)
    var_form.ry(Variable, 0)
    var_form.cx(0, 1)
    var_form.h(1)
    var_form.measure([0, 1], [0, 1])
    return var_form

Variables = [1, 2, 3, 4, 5]

probsu = []
circuits = []
for i in range(len(Variables)):
    circuit = QuantumCircuit(qrz, crz)
    circuit = qc(Variables[i])
    circuits.append(circuit)
    # Issue here: 'counts' is referenced before it is ever defined
    prob = counts['1001'] / sum(counts.values())  # Issue here
    probsu.append(prob)

circuits = transpile(circuits, backend=backend)
job_manager = IBMQJobManager()
MyExperiments = job_manager.run(circuits, backend=backend, name='MyExperiment')
results = MyExperiments.results()
counts = results.get_counts(circuit)
