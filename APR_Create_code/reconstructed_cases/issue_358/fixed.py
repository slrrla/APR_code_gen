# Install qiskit first (run in terminal, not as part of the script):
#   pip install qiskit
# then the import works correctly
from qiskit.circuit.library import MCMTVChain

mcmt = MCMTVChain(gate="cx", num_ctrl_qubits=2, num_target_qubits=1)
print(mcmt)
