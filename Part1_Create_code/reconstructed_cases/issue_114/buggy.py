from qiskit.tools.jupyter import *
from qiskit.test.mock import FakePoughkeepsie

# original user code indexed a list of providers: P[1].get_backend(...)
# reproduced here with a local mock backend instead of a real IBMQ device
backend = FakePoughkeepsie()

# %qiskit_backend_overview is an IPython magic and only works inside
# a Jupyter/IPython session; calling it this way reproduces the reported error
get_ipython().run_line_magic('qiskit_backend_overview', '')
