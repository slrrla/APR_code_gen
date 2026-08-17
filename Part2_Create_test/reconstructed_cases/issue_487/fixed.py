import numpy as np
from docplex.mp.model import Model
from qiskit.optimization import QuadraticProgram

# Manual construction of the docplex model for the specific 3-node path graph problem
mdl = Model('docplex model')
x_0 = mdl.binary_var('x_0')
x_1 = mdl.binary_var('x_1')
x_2 = mdl.binary_var('x_2')
mdl.minimize(-x_0 - x_1 - x_2 + 2*x_0*x_1 + 2*x_2*x_1)
print(mdl.export_as_lp_string())

def the_auto_doco_mod(qubo_array, model_name, constant):
    """
    Function that takes the QUBO array created for a graphing problem and
    converts it to a docplex model ready for qiskit.
    Directly constructs the quadratic program with reference to this page.
    """
    number_of_variables = len(qubo_array[1])  # gets the number of variables from the length of the square qubo matrix
    mod = QuadraticProgram()
    for variable in range(0, number_of_variables):  # creates the binary variables from the size of the matrix
        var_name = "x_" + str(variable)
        mod.binary_var(name=var_name)
    mod.minimize(constant=constant, quadratic=qubo_array)
    # can put in all constraints as quadratic as the binary variables mean that x_0 ^ 2 = x_0 in both cases
    # not sure of the impact of this on performance however
    print(mod.export_as_lp_string())

qubo_array = np.array([[-1, 2, 0],
                        [0, -1, 2],
                        [0, 0, -1]])

the_auto_doco_mod(qubo_array, 'model_name', 2)
