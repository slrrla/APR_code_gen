from qiskit.exceptions import QiskitError

try:
    raise QiskitError("example error")
except QiskitError as e:
    print("Caught error:", e)
