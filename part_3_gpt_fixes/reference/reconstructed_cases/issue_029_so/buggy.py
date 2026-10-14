import subprocess

# The user runs `pip3 install qiskit` from a terminal.
# This installs qiskit into whatever Python installation `pip3`
# happens to point to on the system -- which may not be the same
# Python interpreter that the Jupyter Notebook kernel is using.
subprocess.call(["pip3", "install", "qiskit"])

# Later, inside the Jupyter Notebook, trying to import qiskit fails
# because it was installed into a different Python environment.
import qiskit

print(qiskit.__version__)
