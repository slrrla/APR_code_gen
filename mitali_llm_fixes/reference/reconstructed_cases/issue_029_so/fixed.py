import sys
import subprocess

# Run pip through the same Python interpreter that the Jupyter kernel
# is actually using (sys.executable), instead of relying on whatever
# "pip3" resolves to on the system PATH. This mirrors running
# "!pip3 install qiskit" from inside the notebook itself, ensuring
# qiskit is installed into the kernel's environment.
subprocess.call([sys.executable, "-m", "pip", "install", "qiskit"])

import qiskit

print(qiskit.__version__)
