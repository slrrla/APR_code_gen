from qiskit import *
import numpy as np

def Hamiltonian(n, h):
    pow_n = 2**n
    qc = np.empty(2*n-1, dtype=object)
    # Creating the quantum circuits that are used in the calculation of the Hamiltonian
    # based on the number of qubits
    for i in range(0, 2*n-1):  # 2n-1 is the number of factors on the n-site Hamiltonian
        qr = QuantumRegister(n)
        qc[i] = QuantumCircuit(qr)  # create quantum circuits for each factor of the Hamiltonian
        if (i <= n-2):  # for the first sum of the Hamiltonian
            qc[i].z(i)      # value of current spin
            qc[i].z(i+1)    # and value of its neighboring spin
        else:  # for the second sum of the Hamiltonian
            qc[i].x(2*n-2-i)  # 2*n-2 gives the proper index since counting starts at 0

    # Run each circuit in the simulator
    simulator = Aer.get_backend('unitary_simulator')
    result = np.empty(2*n-1, dtype=object)
    unitary = np.empty(2*n-1, dtype=object)
    Hamiltonian_Matrix = 0
    # Get the results for each circuit in unitary form
    for i in range(0, 2*n-1):
        result[i] = execute(qc[i], backend=simulator).result()
        unitary[i] = result[i].get_unitary()
        # And calculate the Hamiltonian matrix according to the formula
        if (i <= n-2):
            Hamiltonian_Matrix = np.add(Hamiltonian_Matrix, -unitary[i])
        else:
            Hamiltonian_Matrix = np.add(Hamiltonian_Matrix, -h*unitary[i])

    print("The", pow_n, "x", pow_n, "Hamiltonian Matrix is:")
    print(Hamiltonian_Matrix)

    # Now that we have the Hamiltonian, find the eigenvalues and eigenvectors
    w, v = np.linalg.eig(Hamiltonian_Matrix)
    print("Eigenvectors")
    print(v)
    print("Eigenvalues")
    print(w)

    minimum = w[0]
    min_spot = 0
    for i in range(1, pow_n):
        if w[i] < minimum:
            min_spot = i
            minimum = w[i]
    print(min_spot)
    groundstate = v[:, min_spot]
    # the probability to measure each basic state of n qubits
    probability = np.square(groundstate).real
    print("The probability for each of the", pow_n, "base states is:")
    print(probability)
    print("The probabilities for each of the", pow_n, "base states add up to:")
    print("%.2f" % np.sum(probability))

Hamiltonian(3, 1)
