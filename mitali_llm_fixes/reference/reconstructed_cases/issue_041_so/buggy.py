# Buggy: fails with ImportError: cannot import name 'Aer'
# This happens on some Windows/Anaconda or Linux CI setups where the
# qiskit-aer C++/Cython extensions cannot load their native dependency
# (missing openblas.dll / libopenblas), so the Aer submodule fails to import.
from qiskit import Aer
