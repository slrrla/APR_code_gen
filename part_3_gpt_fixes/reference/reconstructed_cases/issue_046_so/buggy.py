# Reconstructed build script for qiskit-aer from source
# Reproduces the reported pybind11 compilation error scenario
import subprocess
import sys

def install_requirements():
    # Author installed requirements per CONTRIBUTING.md but did NOT
    # install the global pybind11 headers, which caused a build error:
    # "an rvalue reference cannot be bound to an lvalue" in
    # aer_state_binding.hpp during compilation of bindings.cc
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"], check=True)

def build_qiskit_aer():
    # Build command with CUDA + MPI options as run by the asker
    cmd = [
        sys.executable, "./setup.py", "bdist_wheel",
        "--", "-DAER_THRUST_BACKEND=CUDA", "-DAER_MPI=True"
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    install_requirements()
    build_qiskit_aer()
