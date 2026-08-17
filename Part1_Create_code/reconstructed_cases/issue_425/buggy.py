from qiskit.circuit.library import EfficientSU2

var_form = EfficientSU2(6, entanglement="linear")
var_form_inv = var_form.inverse()  # error thrown of this line
