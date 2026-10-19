from qiskit.opflow import X, Y, Z, I

H = 5.9*(I^I^I) + 0.21*(Z^I^I) - 6.12*(I^Z^I) - 2.14*(X^X^I) - 2.14*(Y^Y^I) + 9.6*(I^I^I) - 9.6*(I^I^Z) - 3.9*(I^X^X) - 3.9*(I^Y^Y)

from qiskit.visualization.array import array_to_latex
H_matrix = H.to_matrix()
array_to_latex(H_matrix)
