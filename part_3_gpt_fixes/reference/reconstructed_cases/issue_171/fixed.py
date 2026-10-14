# Corrected computation of the average fidelity of a Pauli error channel
# with probabilities px, py, pz.
#
# Step 1: entanglement fidelity F_e = 1 - (px + py + pz)
# Step 2: Horodecki's formula relates F_e to the average fidelity F_avg
#         for an N-dimensional system:
#           F_avg = (N * F_e + 1) / (N + 1)
# For a single qubit N = 2, giving:
#           F_avg = 1 - (2/3) * (px + py + pz)

px = 0.02
py = 0.03
pz = 0.05

def entanglement_fidelity(px, py, pz):
    return 1 - (px + py + pz)

def average_fidelity(px, py, pz, N=2):
    Fe = entanglement_fidelity(px, py, pz)
    return (N * Fe + 1) / (N + 1)

F_avg = average_fidelity(px, py, pz)
print("Average fidelity (fixed):", F_avg)
