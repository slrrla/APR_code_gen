# Group 4 final notes

Twenty standalone tests were added for 736, 752, 774, 791, 797, 814, 823, 859,
863, 870, 879, 892, 902, 924, 974, 981, 992, 1001, 1009, and 1033. The final
parent matrix in `../results.json` is authoritative. Original buggy/fixed
sources were not modified.

- 814 uses deterministic missing/present count dictionaries at the Result
  boundary while still executing the original circuit. This specifically tests
  absent-key handling without hoping a random 41-shot sample omits 011.
- 859 seeds NumPy's default RNG and observes actual Statevector evolution over
  several seeds. Reset is never replaced by a projector in the test.
- 892: fixed returns only one per-shot state in Aer 0.8 / Qiskit 0.25.0, but ten
  in the workbook's 0.46.3 environment. The test retains the ten-shot requirement.
- 981: a unit-cell orientation reversal places intercell coupling 2 on different
  matrix diagonals. Both physically equivalent SSH basis conventions are
  accepted; requiring strictly alternating immediate array diagonals was an
  oracle overconstraint that was corrected. This pair is reconstructed from an
  explanatory question rather than an original executable buggy program.
- 1001: old Aer lacks QuantumError.from_dict, while newer Aer requires it for
  instruction dictionaries. Capability detection reconstructs the same noise
  channel in both versions. The test checks warning suppression and physical
  composition; it does not merely assert the warnings=False source text.
- 1009 was strengthened after generation: it observes real finite-shot execution
  and Result counts, accepts a sampled mean of zero, and does not require a
  particular converter class. It separates in 0.46.3. Both programs legitimately
  sample in 0.25.0. The final test file supersedes its initial builder draft.
- 1033 checks the original GHZ preparation question. Both constructions prepare
  the same GHZ state from 000; forcing full-operator equality would be wrong.
  The reconstructed assignment typo is not treated as a source-grounded APR bug.

Actual final tests are the sibling case folders' test.py files. Builder scripts
are initial authoring records, not a replacement for the validated final tests.
