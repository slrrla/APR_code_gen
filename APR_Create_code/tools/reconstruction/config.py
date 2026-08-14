"""Central configuration for the Qiskit APR reconstruction pipeline.

Every tunable lives here so a policy change is a config edit, not a code edit.
"""
from __future__ import annotations

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKBOOK = PROJECT_ROOT / "Qiskit_562_and_556_code_generation_cases (1).xlsx"

#: The ONLY worksheet that may be read. Enforced in loader.py.
SOURCE_SHEET = "556_confirmed_qiskit"

#: Sheets that are explicitly forbidden as data sources.
FORBIDDEN_SHEETS = ("Summary", "562_all_nonvisual_both_code")

OUTPUT_DIR = PROJECT_ROOT / "reconstructed_cases"
REPORT_CSV = OUTPUT_DIR / "reconstruction_report.csv"
STATE_DIR = PROJECT_ROOT / "tools" / "reconstruction" / ".state"
CHECKPOINT = STATE_DIR / "checkpoint.jsonl"
#: Raw model responses, keyed by case. Makes resume free and runs auditable.
LLM_CACHE_DIR = STATE_DIR / "llm_cache"

EXPECTED_ROW_COUNT = 556

# --------------------------------------------------------------------------
# Directory naming
# --------------------------------------------------------------------------
# issue_number is NOT unique in the source sheet: SE and SO cases were numbered
# independently, so 25 numbers appear twice (531 unique values / 556 rows).
# (platform, issue_number) IS unique across all 556 rows.
#
#   "suffix_collisions" -> issue_005_se / issue_005_so only where they collide,
#                          plain issue_NNN everywhere else.  [default]
#   "prefix_platform"   -> issue_se_005 / issue_so_005 for every row.
#   "append_issue_id"   -> issue_005__40286 for every row.
#   "number_only"       -> issue_005 always; collisions overwrite. LOSSY.
NAMING_SCHEME = "suffix_collisions"

#: Minimum zero-padding width for issue_number in directory names.
PAD_WIDTH = 3

# --------------------------------------------------------------------------
# Artifact filenames
# --------------------------------------------------------------------------
BUGGY_FILE = "buggy.py"
FIXED_FILE = "fixed.py"
QUESTION_FILE = "original_question.txt"

# --------------------------------------------------------------------------
# LLM reconstruction
# --------------------------------------------------------------------------
#: Semantic reconstruction is the model's job. Static analysis validates and
#: cleans the result; it never substitutes for it.
LLM_MODEL = os.environ.get("APR_LLM_MODEL", "claude-sonnet-5")
LLM_MAX_TOKENS = int(os.environ.get("APR_LLM_MAX_TOKENS", "8000"))
#: Newer Claude models reject an explicit temperature; None omits the field.
LLM_TEMPERATURE = None
LLM_MAX_RETRIES = 4
LLM_RETRY_BASE_DELAY = 2.0
LLM_TIMEOUT_S = 180

#: Per-field character budget in the prompt. Longer cells are middle-truncated
#: with an explicit marker so the model knows material was elided.
FIELD_CHAR_BUDGET = {
    "title": 400,
    "category_label": 200,
    "buggy_question_description": 14000,
    "buggy_code": 14000,
    "fixed_solution_explanation": 14000,
    "fixed_code": 14000,
}

#: One repair round-trip is allowed when the model returns unparseable Python.
LLM_REPAIR_ATTEMPTS = 1

#: Provider: "anthropic" for real calls, "stub" for offline plumbing tests.
LLM_PROVIDER = os.environ.get("APR_LLM_PROVIDER", "anthropic")

# --------------------------------------------------------------------------
# Execution sandbox
# --------------------------------------------------------------------------
EXEC_TIMEOUT_SECONDS = 30
#: Master switch. When False the pipeline is static-analysis only.
ENABLE_EXECUTION = True
#: Symbols whose presence means the program wants remote/hardware access.
#: Such programs are never executed; they are reported as SKIPPED_NETWORK.
NETWORK_SYMBOLS = (
    "QiskitRuntimeService",
    "IBMQ",
    "IBMProvider",
    "least_busy",
    "save_account",
    "enable_account",
    "load_account",
    "IBMQFactory",
    "ibm_quantum",
    "requests.get",
    "requests.post",
    "urlopen",
)

# --------------------------------------------------------------------------
# Reconstruction policy
# --------------------------------------------------------------------------
#: Upper bound on generated program size. Larger => flagged as suspicious.
MAX_REASONABLE_LINES = 400
#: Max lines the syntax-repair loop is allowed to drop before giving up.
MAX_REPAIR_DROPS = 25

#: Separator token the scraper injected between distinct code blocks in a cell.
#: 4,425 occurrences across the sheet, so it is handled explicitly rather than
#: being left for the cleaner to trip over.
CODE_BLOCK_SEPARATOR = "---CODE_BLOCK---"

#: Markers after which `category` text stops being a taxonomy label and becomes
#: verdict prose. Trimmed purely to keep the prompt focused; 79% of non-empty
#: category cells carry this tail.
CATEGORY_LEAK_MARKERS = (
    "why ai wins",
    "why stack overflow wins",
    "why the ai",
    "winner:",
    "verdict",
    "summary comparison",
    "the ai solution",
    "stack overflow wins",
    "ai wins",
)
CATEGORY_LABEL_MAX_CHARS = 120
