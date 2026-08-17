import subprocess

# Clone the full repository so the notebooks (in qiskit-textbook/content)
# are available locally, then install the package from the local source.
subprocess.run(
    "git clone https://github.com/qiskit-community/qiskit-textbook.git",
    shell=True,
    check=True,
)
subprocess.run(
    "cd qiskit-textbook && pip install ./qiskit-textbook-src",
    shell=True,
    check=True,
)

# Notebooks with the textbook content are now available under:
# qiskit-textbook/content

# Optionally, the qiskit tutorials can also be fetched separately:
subprocess.run(
    "git clone https://github.com/Qiskit/qiskit-tutorials.git",
    shell=True,
    check=True,
)

# Tutorials are then found under: tutorials
