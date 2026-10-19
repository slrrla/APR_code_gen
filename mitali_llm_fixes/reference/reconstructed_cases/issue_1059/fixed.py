from qiskit import QuantumCircuit, execute, Aer
from qiskit.compiler import transpile

backend = Aer.get_backend('qasm_simulator')

def qc(Variable):
    var_form = QuantumCircuit(2, 2)
    var_form.ry(Variable, 0)
    var_form.cx(0, 1)
    var_form.h(1)
    var_form.measure([0, 1], [0, 1])
    return var_form

Variables = [1, 2, 3, 4, 5]

circuits = []
for i in range(len(Variables)):
    circuit = QuantumCircuit(2, 2)
    circuit = qc(Variables[i])
    circuits.append(circuit)

circuits = transpile(circuits, backend=backend)
job = execute(circuits, backend=backend, shots=1000)
results = job.result()

probsu = []
for i in range(len(Variables)):
    counts = results.get_counts(i)
    prob = counts['11'] / sum(counts.values())
    probsu.append(prob)

print('probability of getting |11> at each circuit:', probsu)
