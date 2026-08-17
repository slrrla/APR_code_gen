# Reconstructed build script for qiskit-aer from source
# Fix: install pybind11 with the "global" extra so the correct
# pybind11 headers are used, resolving the rvalue/lvalue binding error
import subprocess
import sys

def install_requirements():
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"], check=True)
    # Fix applied: install pybind11[global] before building
    subprocess.run([sys.executable, "-m", "pip", "install", "pybind11[global]"], check=True)

def build_qiskit_aer():
    cmd = [
        sys.executable, "./setup.py", "bdist_wheel",
        "--", "-DAER_THRUST_BACKEND=CUDA", "-DAER_MPI=True"
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    install_requirements()
    build_qiskit_aer()
