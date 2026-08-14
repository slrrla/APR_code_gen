import json
from qiskit.assembler.disassemble import disassemble
from qiskit.qobj import QasmQobj

# Minimal placeholder standing in for the downloaded IBM job.json payload
job_json = {
    "qobj_id": "1",
    "header": {},
    "config": {"shots": 1, "memory_slots": 1, "n_qubits": 1},
    "schema_version": "1.3.0",
    "type": "QASM",
    "experiments": [
        {
            "instructions": [
                {"name": "rz", "params": [1.5707963267948966], "qubits": [0]},
                {"name": "sx", "qubits": [0]},
                {"name": "measure", "qubits": [0], "memory": [0]}
            ],
            "header": {"n_qubits": 1, "memory_slots": 1},
            "config": {"n_qubits": 1, "memory_slots": 1}
        }
    ]
}

with open('job.json', 'w') as fd:
    json.dump(job_json, fd)

with open('job.json') as fd:
    qobj_dict = json.load(fd)

qobj = QasmQobj.from_dict(qobj_dict)
circuits, run_config, headers = disassemble(qobj)

circuit = circuits[0]
print(circuit)
