# The user installed the qiskit-textbook package via pip:
#   pip install git+https://github.com/qiskit-community/qiskit-textbook.git#subdirectory=qiskit-textbook-src
#
# They do not know where the package was installed on disk.
# This script attempts to import it and print its file location,
# but does not use any tool to query installed package metadata.

import qiskit_textbook

print(qiskit_textbook.__file__)
