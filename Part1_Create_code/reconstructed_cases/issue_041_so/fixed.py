# Fixed: the import itself does not change. The actual fix was environmental:
# installing the missing OpenBLAS shared library (openblas.dll on Windows,
# libopenblas-dev on Linux/Travis CI) so that the compiled qiskit-aer
# extension modules (qasm_controller_wrapper, statevector_controller_wrapper,
# unitary_controller_wrapper) can load their native dependency correctly.
#
# Once OpenBLAS is available on the system, the same import succeeds:
from qiskit import Aer
