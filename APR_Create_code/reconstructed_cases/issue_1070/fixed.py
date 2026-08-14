import numpy as np
import qiskit.quantum_info as qi

# Process matrix - this is a Pauli Transfer Matrix
process = np.array([[ 1.   ,  0.   ,  0.   ,  0.   ],
                     [ 0.001,  0.986,  0.02 ,  0.04 ],
                     [ 0.014,  0.01 ,  0.019, -0.957],
                     [-0.028, -0.031,  0.949,  0.008]])

# FIX: interpret the matrix as a PTM, which correctly converts it to a
# valid superoperator representation before extracting Kraus operators
q_process = qi.PTM(process)
kraus_ = qi.Kraus(q_process)
print(kraus_)

kraus_list = kraus_.data

sum_of_kraus = np.zeros((2, 2), dtype=complex)
for k in kraus_list:
    sum_of_kraus += np.matmul(k.conj().T, k)

print(sum_of_kraus)
