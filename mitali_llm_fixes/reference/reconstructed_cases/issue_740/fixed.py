from qiskit.providers.fake_provider import FakeLima
from qiskit.visualization import plot_error_map

backend = FakeLima()
plot_error_map(backend)
