# Experiment protocol

## Research objective

Evaluate whether an evidence-driven conformance harness makes known module nonconformances more observable and diagnosable than a minimal document-and-happy-path integration baseline.

## Study boundary

The system under test is a synthetic, stateless sensor-event processing interface. No operational, classified, proprietary, export-controlled, or controlled-unclassified data are used.

## Units and conditions

- Primary unit: one unique candidate module package.
- Candidates: two conformant controls and eighteen single-fault candidates.
- Within-unit comparison: each candidate is assessed by both the baseline and the harness.
- Repeated executions: twenty per method/candidate for timing and decision-stability analysis only.
- Random seed: `20260623`.
- Fixed vectors: eight.
- Generated vectors per harness run: forty-eight.

## Primary outcome

Fault-detection sensitivity among the eighteen faulted candidates.

## Secondary outcomes

Control acceptance, actionable diagnosis accuracy, evidence completeness, checks/tests executed, runtime, decision stability, evidence-digest stability, and sensitivity of decisions to random dimension weights.

## Statistical analysis

- Wilson score intervals for binomial proportions.
- Exact McNemar test for paired correctness decisions across unique candidate packages.
- Paired Wilcoxon signed-rank test for candidate-level median runtime.
- Cliff's delta as a distributional effect-size description for candidate-level median runtime.
- Ten thousand Dirichlet weight draws to examine score-only and gate-adjusted decision sensitivity.

## Decision rule

The harness passes a candidate only when the weighted composite score is at least 80 and no high- or critical-severity gate has failed. The gate rule is pre-specified to prevent strong performance in one dimension from compensating for a decisive interface, provenance, security, or semantic defect.

## Interpretation limits

The design supports feasibility and internal comparison within the supplied fault model. It does not estimate program-level cost savings, field integration time, human labor, or mission effectiveness.
