"""Configuration for the multi-version Qiskit execution matrix."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = PROJECT_ROOT / "reconstructed_cases"
ENVS_DIR = PROJECT_ROOT / "envs"
ENV_MANIFEST = ENVS_DIR / "manifest.json"
ENV_SPEC = ENVS_DIR / "spec.json"

STATE_DIR = PROJECT_ROOT / "tools" / "execution" / ".state"
RESULTS_JSONL = STATE_DIR / "execution_results.jsonl"
ORACLE_DIR = STATE_DIR / "oracles"
WORKDIR_ROOT = STATE_DIR / "workdirs"

EXECUTION_CSV = PROJECT_ROOT / "execution_results.csv"
EXCEL_WORKBOOK = PROJECT_ROOT / "qiskit_version_validation.xlsx"

BUGGY_FILE = "buggy.py"
FIXED_FILE = "fixed.py"

#: Per-program wall-clock limit. Old simulators are slow; 60s keeps a hung
#: program from stalling a 30k-execution matrix.
EXEC_TIMEOUT_SECONDS = int(os.environ.get("APR_EXEC_TIMEOUT", "60"))

#: Captured stream text is truncated before it reaches the CSV so one noisy
#: traceback cannot bloat the corpus-wide export.
MAX_CAPTURE_CHARS = 4000

#: Parallel worker processes for the matrix. Each runs one program.
DEFAULT_WORKERS = int(os.environ.get("APR_EXEC_WORKERS", "4"))

CONDA = os.environ.get("APR_CONDA", "conda")

#: Programs referencing these want remote/hardware access and are never run.
NETWORK_SYMBOLS = (
    "QiskitRuntimeService", "IBMQ", "IBMProvider", "least_busy",
    "save_account", "enable_account", "load_account", "IBMQFactory",
    "ibm_quantum", "requests.get", "requests.post", "urlopen",
)

#: Import failures naming these are genuine Qiskit-version incompatibility.
QISKIT_FAMILY = (
    "qiskit", "qiskit_aer", "qiskit_algorithms", "qiskit_ibm_runtime",
    "qiskit_ibm_provider", "qiskit_ibmq_provider", "qiskit_nature",
    "qiskit_optimization", "qiskit_machine_learning", "qiskit_finance",
    "qiskit_experiments", "qiskit_dynamics",
)

#: Import failures naming these are gaps in OUR environment, not Qiskit history.
THIRD_PARTY_HINTS = (
    "pennylane", "torch", "tensorflow", "networkx", "iqx", "pylatexenc",
    "seaborn", "pandas", "cvxpy", "qutip", "sklearn", "scikit", "numba",
    "docplex", "cplex", "gurobi", "pyscf", "openfermion", "PIL", "pillow",
)

# -- oracle -----------------------------------------------------------------
ORACLE_MODEL = os.environ.get("APR_ORACLE_MODEL", "claude-sonnet-5")
ORACLE_MAX_TOKENS = 1200
