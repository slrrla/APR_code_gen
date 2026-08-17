from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def circuit():
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    circuit = QuantumCircuit(qr, cr)
    circuit.x(qr[1])
    circuit.x(qr[0]).c_if(cr, 1)  # c_if(cr, 2) mean Cr= 010 if a<b
    circuit.x(qr[0])
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit

# Local simulator used instead of a real IBM hardware backend
backend = AerSimulator()

qc_transpiled1 = transpile(circuit(), backend)
qc_transpiled2 = transpile(circuit(), backend)
qc_transpiled3 = transpile(circuit(), backend)

# FIX: build a list of circuits instead of a tuple
circuits = []
circuits.append(qc_transpiled1)
circuits.append(qc_transpiled2)
circuits.append(qc_transpiled3)
job = backend.run(circuits, shots=20000, dynamic=True)
job.job_id()
