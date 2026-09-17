# Batch04 case summary

| Case | What is checked | Versions | Fixed result |
|---|---|---:|---|
| 504 | Register ownership, real Aer sampling, and exact oracle phase marking | 23 | Construction/sampling pass; oracle semantics fail |
| 505 | Scalar composition retains an operator with diagonal entries 4x and 0 | 8 | All pass |
| 565 | Nine-qubit QAOA circuit construction and feasible-tour mixer transitions | 4 | Construction passes; mixer semantics fail |
| 595 | Aer returns the complete Hadamard-CNOT unitary | 23 | All pass |
| 596 | Four parameter values produce the expected operator and numeric Qobj | 12 | All pass |
| 600 | Six fractional Pauli interactions and sampled output probability | 12 | All pass; early buggy versions have an import mismatch |
| 622 | Backend capacity and 1024-shot Bell correlations | 12 | All pass |
| 624 | Circuit-to-operator conversion and local QAOA state/energy consistency | 12 | All pass; no global-optimum claim |
| 635 | Conditional AND behavior across all eight input basis states | 4 | All pass |
| 662 | Printed totals h=4, cx=3, rz=1, measure=4 | 23 | All pass; buggy fails at obsolete DAG-node access |

504 and 565 are REVIEW FIXED because broader semantic checks fail even though the original
construction/interface repairs work. They are different from 018_se's REVIEW EXECUTION,
where the original Aer process crashes before sampled results are available.
