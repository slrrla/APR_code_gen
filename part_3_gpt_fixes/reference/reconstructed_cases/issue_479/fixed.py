from qiskit.providers.models import BackendProperties
from qiskit_aer import AerSimulator
from qiskit_aer.backends.backendconfiguration import AerBackendConfiguration
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService, IBMBackend
import datetime as dt


def simulator_from_backend(backend: IBMBackend, datetime: dt.datetime, **options):
    configuration = AerBackendConfiguration(
        backend_name=f"aer_simulator_from({backend.name})",
        backend_version=backend.backend_version,
        n_qubits=backend.num_qubits,
        basis_gates=backend.operation_names,
        gates=[],
        max_shots=int(1e6),
        coupling_map=list(backend.coupling_map.get_edges()),
        max_experiments=backend.max_circuits,
        description=f"{backend.name} in {datetime}",
    )
    properties = BackendProperties.from_dict(backend.properties(datetime=datetime).to_dict())
    target = backend.target_history(datetime=datetime)
    options["noise_model"] = NoiseModel.from_backend_properties(properties)
    return AerSimulator(configuration=configuration, properties=properties, target=target, **options)


# Fixing the calibration datetime makes the simulator reproducible in the future.
service = QiskitRuntimeService(channel="ibm_quantum", token="MY_TOKEN")
backend = service.backend('ibm_sherbrooke')
datetime = dt.datetime(2024, 8, 1)
simulator = simulator_from_backend(backend, datetime)
