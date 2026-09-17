# Batch05 case summary

| Case | Verification | Versions | Fixed |
|---|---|---:|---|
| 663 | Measurements and complete prepared state | 8 | All pass |
| 671 | Register identity/order and all basis mappings | 27 | All pass |
| 727 | Bound exponential controlled phases | 12 | All pass |
| 742 | Observable conversion and actual local EstimatorV2 result | 12 | All pass with task-local Runtime dependencies |
| 747 | 100000-shot GHZ counts and exact state | 8 | All pass |
| 750 | Complete subsystem operator and tensor alternatives | 23 | All pass; review original APR suitability |
| 769 | Standard-gate recognition and unmatched matrices | 15 | All pass; buggy import fails before original behavior |
| 773 | Local job and real quiet monitor | 8 | All pass; buggy legacy import fails first |
| 775 | OpenQASM parsing, operator, and successful local job | 12 | All pass |
| 795 | Gate, inverse, and coherent controlled operation | 12 | All pass |

No new fixed failures are added. Existing fixed failures and 018_se native-execution errors
remain in the cumulative report. PASS here applies to the stated tests, not to broader
claims such as noisy fidelity, arbitrary gate recognition, or the validity of every case as APR.
