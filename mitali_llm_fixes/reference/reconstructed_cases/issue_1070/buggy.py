import numpy as np
import qiskit.quantum_info as qi

# Process matrix (this is actually a Pauli Transfer Matrix, not a superoperator matrix)
process = np.array([[ 1.   ,  0.   ,  0.   ,  0.   ],
                     [ 0.001,  0.986,  0.02 ,  0.04 ],
                     [ 0.014,  0.01 ,  0.019, -0.957],
                     [-0.028, -0.031,  0.949,  0.008]])

# BUG: interpreting a Pauli transfer matrix directly as a SuperOp
q_process = qi.SuperOp(process)
kraus_ = qi.Kraus(q_process)
print(kraus_)

kraus_list = kraus_.data

sum_of_kraus = np.zeros((2, 2), dtype=complex)
for k in kraus_list:
    sum_of_kraus += np.matmul(k.conj().T, k)

print(sum_of_kraus)
