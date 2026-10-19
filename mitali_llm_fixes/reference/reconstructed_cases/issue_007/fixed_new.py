import ast
from qiskit.result import Result

payload = {
    "backend_name": "ibmq_16_melbourne",
    "backend_version": "1.1.0",
    "qobj_id": "qobj_0",
    "job_id": "job_0",
    "success": True,
    "results": [
        {
            "shots": 1024,
            "success": True,
            "header": {"memory_slots": 2, "name": "circuit-0"},
            "data": {"counts": {"0x0": 512, "0x3": 512}},
        }
    ],
}

res = Result.from_dict(payload)

# Serialize the dictionary representation, not Result.__repr__()
serialised = res.to_dict()

with open("result.txt", "w") as f:
    f.write(str(serialised))

with open("result.txt") as f:
    line = f.read()

# SO used eval(line); literal_eval is the safer equivalent here
restored = Result.from_dict(ast.literal_eval(line))

print(restored.get_counts())