# Data dictionary

## `results/primary_results.csv`

| Field | Definition |
|---|---|
| `candidate` | Unique candidate module package. |
| `fault_class` | Intended single nonconformance class, or `control`. |
| `expected_conformant` | Ground-truth status established by construction. |
| `method` | `baseline` or `harness`. |
| `passed` | Method decision. |
| `correct_decision` | Whether the decision matches ground truth. |
| `detected_nonconformance` | True when a faulted candidate is rejected. |
| `duration_ms` | Wall-clock evaluation duration in milliseconds. |
| `findings_count` | Number of recorded findings. |
| `actionable_diagnosis` | Highest-priority diagnosed root-cause category. |
| `diagnosis_correct` | Whether the diagnosis matches the injected fault class. |
| `evidence_completeness` | Fraction of expected evidence items present. |
| `tests_or_checks` | Number of executed checks or tests. |
| `*_score` | Harness dimension or composite score on a 0-100 scale. |
| `evidence_confidence` | Evidence completeness adjusted for test-volume sufficiency. |
| `gate_failure` | Whether a high- or critical-severity condition blocks passage. |
| `evidence_digest` | SHA-256 digest of the canonicalized harness evidence package. |

## `results/repeated_runs.csv`

Contains repeated timing, decision, and digest observations. Repeated rows are not independent fault cases and are not used to inflate the sample size for sensitivity inference.

## `results/statistical_summary.json`

Contains method-level binomial estimates, paired tests, reliability summaries, runtime effects, and the weight-sensitivity experiment.
