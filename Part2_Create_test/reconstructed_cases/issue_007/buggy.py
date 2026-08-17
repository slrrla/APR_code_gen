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

with open("result.txt", "w") as f:
    f.write(res)

with open("result.txt") as f:
    line = f.read()

restored = Result.from_dict(line)
print(restored.get_counts())
