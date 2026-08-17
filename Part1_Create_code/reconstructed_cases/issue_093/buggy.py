import subprocess

# Author's original installation approach for the qiskit_textbook package
# This only installs the package itself; it does not fetch the
# accompanying Jupyter notebooks, which was the reported problem.
subprocess.run(
    "pip install git+https://github.com/qiskit-community/qiskit-textbook.git#subdirectory=qiskit-textbook-src",
    shell=True,
    check=True,
)
