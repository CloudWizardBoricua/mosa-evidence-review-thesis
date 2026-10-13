# MOSA Conformance Harness Prototype (Thesis Research Artifact)

Version 1.0.0 accompanies the thesis **A Conformance Harness for Verifiable Modular Open Systems Outcomes in Defense Acquisition: Design, Implementation, and Controlled Evaluation**.

This repository is a **controlled, non-sensitive research prototype** used to evaluate whether machine-readable interface contracts, structured evidence, substitution tests, and automated conformance checks detect known integration defects more reliably than a minimal document-and-happy-path baseline.

## Important scope statement

The repository does not contain classified, controlled unclassified, export-controlled, proprietary, or operational Department of Defense data. Results are from a synthetic sensor-processing mission thread and must not be represented as field validation of a DoD program. The unit of analysis is a candidate module package, not a weapon system or acquisition program.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m mosa_harness.experiment --root . --repeats 20 --seed 20260623
PYTHONPATH=src python -m mosa_harness.analysis --root .
PYTHONPATH=src python -m mosa_harness.figures --root .
PYTHONPATH=src pytest -q
```

A convenience script is also provided:

```bash
./run_all.sh
```

## Artifact structure

- `schemas/`: machine-readable input, output, and manifest contracts.
- `candidate_modules/`: two independently implemented conformant controls and eighteen fault-injected candidates.
- `src/mosa_harness/`: baseline evaluator, conformance harness, experiment runner, analysis, and figure generation.
- `test_vectors/`: fixed acceptance vectors; additional property-oriented vectors are generated from the recorded seed.
- `results/`: primary decisions, repeated-run timing, statistical summaries, figures, and per-candidate evidence packages.
- `tests/`: executable acceptance and reproducibility tests.
- `EXPERIMENT_PROTOCOL.md`: pre-specified conditions, variables, and analysis rules.
- `DATA_DICTIONARY.md`: definitions for the principal result fields.
- `SHA256SUMS.txt`: integrity hashes for the packaged artifact.

## Research design

The primary unit of analysis is a unique candidate module package. The two methods evaluate the same twenty candidates. Primary fault-detection inference uses the unique candidates; twenty repeated executions are used only for timing and reproducibility analysis so repeated runs are not treated as independent fault cases. The baseline performs manifest presence, import, and one happy-path schema/shape check. The harness adds provenance validation, manifest and output-schema validation, dependency inspection, security checks, fixed and generated semantic tests, determinism checks, latency checks, evidence completeness, scoring, and non-compensable gates.

## Main result

In the recorded run, the baseline detected 5 of 18 injected nonconformances, while the harness detected 18 of 18. Both methods accepted the two conformant controls. These results establish feasibility within the synthetic study boundary; they do not establish operational effectiveness, lifecycle savings, or external validity for DoD programs.
