# User has a binary matrix describing an encoder (from a non-python QECC tool)
# but no way (yet) to turn it into a stim/qiskit Tableau or Circuit.
matrix = [
    [0,0,0,0,0,1,1,1,1,1],
    [1,0,0,0,1,0,0,1,1,0],
    [0,1,0,0,1,1,1,1,0,1],
    [0,0,1,0,1,0,1,1,1,1],
    [0,0,0,1,1,1,1,0,0,0],
    [0,0,0,0,1,0,1,1,0,0],
    [0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,1,0],
]

print(matrix)
