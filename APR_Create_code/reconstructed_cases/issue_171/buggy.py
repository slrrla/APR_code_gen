# Reproduces an attempt to compute the average fidelity of a Pauli error
# channel with probabilities px, py, pz using the (wrong) assumption that
# the average fidelity equals the entanglement fidelity:
#   F_avg = 1 - (px + py + pz)
# This omits the factor of 2/3 required by Horodecki's formula.

px = 0.02
py = 0.03
pz = 0.05

def average_fidelity(px, py, pz):
    # BUG: this is actually the entanglement fidelity, not the average fidelity
    return 1 - (px + py + pz)

F_avg = average_fidelity(px, py, pz)
print("Average fidelity (buggy):", F_avg)
