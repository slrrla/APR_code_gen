import json
from qiskit import QuantumCircuit

# Minimal placeholder standing in for the downloaded IBM job.json payload
job_json = {
    "config": {"n_qubits": 1, "memory_slots": 1},
    "header": {"n_qubits": 1, "memory_slots": 1},
    "instructions": [
        {"name": "rz", "params": [1.5707963267948966], "qubits": [0]},
        {"name": "sx", "qubits": [0]},
        {"name": "measure", "qubits": [0], "memory": [0]}
    ]
}

with open('job.json', 'w') as fd:
    json.dump(job_json, fd)

with open('job.json') as fd:
    data = json.load(fd)

qc = QuantumCircuit(data['config']['n_qubits'], data['config']['memory_slots'])

# Hand-rolled parser (the "write your own parser" approach from the question)
# BUG: forgets to pass the rotation angle contained in "params"
for instr in data['instructions']:
    name = instr['name']
    qubits = instr['qubits']
    if name == 'rz':
        qc.rz(qubits[0])  # missing angle argument -> wrong/broken circuit
    elif name == 'sx':
        qc.sx(qubits[0])
    elif name == 'measure':
        qc.measure(qubits[0], instr['memory'][0])

print(qc)
