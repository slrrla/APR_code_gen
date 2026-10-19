from qiskit import QISKitError

try:
    raise QISKitError("example error")
except QISKitError as e:
    print("Caught error:", e)
