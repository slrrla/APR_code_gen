# APR LLM repair results

This bundle contains the prompts, generated fixes, test runs, logs, and result
workbooks for the 73-case Qiskit repair experiment.

## Layout

- `results/`: ten current result workbooks, including the seven per-model
  workbooks and comparison summaries. `results/previous/` contains historical
  copies.
- `model_runs/`: model-specific generation files, fixes, testing records, and
  logs. `model_runs/_shared/` contains the shared prompt and assigned-version
  inputs.
- `reference/reconstructed_cases/`: case questions, buggy and human-fixed
  programs, test oracles, and supporting files.
- `reference/Valid_Cases_104.xlsx`: the source for assigned Qiskit versions.
- `Part1_Create_code/` and `Part2_Create_test/` at the repository root:
  project source and case-generation/testing material.
- `model_runs/saumya_verification/`: independent rerun and comparison evidence.

## Models

- GPT-5.6 Luna
- GPT-6 Luna
- GPT-6.1 Sol
- GPT-6 Astra
- Claude Opus 5.5
- Claude Sonnet 5.5
- Claude Haiku 5.5

Generation uses the shared repair prompt with medium thinking effort. Testing
uses the case-specific oracle and the Qiskit versions assigned in
`Valid_Cases_104.xlsx`. The saved logs provide execution evidence; result
labels and test-sensitive notes should be read alongside those logs.

Reproducing the runs requires the appropriate Python/Qiskit environments and
model API credentials. Some historical scripts and logs contain
machine-specific paths, so paths must be adjusted on another computer.

For workbook export, install Node.js and make it available on `PATH`, or set
`APR_NODE_EXE` to its executable. Exporters using `@oai/artifact-tool` also
accept `APR_NODE_MODULES` pointing to a directory containing that package.
The two derived review JSON files have local attachment paths redacted;
their classifications and the raw test logs are unchanged.
