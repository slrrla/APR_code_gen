from qiskit.circuit.library import EfficientSU2

var_form = EfficientSU2(6, entanglement="linear")
# build the circuit so its internal data is populated
var_form._build()
# or just print it
print(var_form)
var_form_inv = var_form.inverse()
