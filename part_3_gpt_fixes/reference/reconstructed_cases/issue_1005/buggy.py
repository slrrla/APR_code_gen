from qiskit.providers.fake_provider import GenericBackendV2

# Create a custom fake backend with basic characteristics
num_qubits = 5
basis_gates = ["id", "rz", "sx", "x", "cx"]
coupling_map = [[0, 1], [1, 2], [2, 3], [3, 4]]

backend = GenericBackendV2(
    num_qubits=num_qubits,
    basis_gates=basis_gates,
    coupling_map=coupling_map,
)

# There is no direct way to set T1/T2 times, qubit frequencies,
# or measurement errors manually with GenericBackendV2.
# The properties are randomly sampled from historical IBM backend data.
print(backend.properties())
