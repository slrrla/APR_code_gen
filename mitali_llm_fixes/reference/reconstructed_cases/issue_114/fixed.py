from qiskit.tools import backend_monitor
from qiskit.test.mock import FakePoughkeepsie

backend = FakePoughkeepsie()

# use the plain python function instead of the Jupyter-only magic;
# it gives the same information without requiring an IPython environment
backend_monitor(backend)
