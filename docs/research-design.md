# Research Design

The study asks whether choosing checks improves evidence review and which fixed safeguards are needed. It allows the conclusion that explicit rules offer the same benefit as a model at lower cost.

## Three methods, shared checks

| Method | What chooses the checks | What stays the same |
| --- | --- | --- |
| Fixed workflow | Always requests every check | Evidence inputs, validators, report format, and decision guard |
| Rule based adaptive workflow | Explicit rules choose the order and stop when evidence is insufficient | Evidence inputs, validators, report format, and decision guard |
| Model agent | The configured model selects permitted checks within a bounded loop | Evidence inputs, validators, report format, and decision guard |

The three shared tools inspect the evidence package, check interface consistency, and verify the software inventory. Software Bill of Materials, or SBOM, means the list of software components. The interface describes how components communicate.

## Case composition

The new benchmark contains 40 neutral case identifiers: 10 ready cases, 20 cases with known problems, and 10 cases requiring further review. Twenty are development cases. Twenty additional cases form a separate reported split and support the primary evaluation.

Expected answers are stored separately from model inputs. Cases, labels, prompts, and settings are frozen before measured execution. A freeze records hashes of the files so a later reader can detect changes. An offline preflight found a structural error in the source fingerprint record, which was corrected before the final freeze and before hosted requests. The additional-case split is therefore not untouched external evaluation evidence. The preflight record is preserved separately and excluded from the final comparison. Independent label review remains pending until a named reviewer and date are recorded.

Run each method three times per case. The planned complete comparison is 360 runs: 40 cases times three methods times three repeats. Count unique cases for accuracy. Use repeats for timing and decision stability. Report stopped and failed runs rather than removing them from the record.

!!! info "Blue: why separate the cases?"
    Development examples help an author build the method. A separately reported set provides another comparison, but an offline preflight was also used to correct a shared defect. Keeping the split and the amendment visible helps a reader assess how much the observed result depends on development choices.

## Measurements

| Measure | Interpretation |
| --- | --- |
| Raw and guarded recommendation correctness | Agreement with the expected answer before and after fixed checks |
| Missed and extra findings | Known issues omitted and unsupported issues added |
| Valid evidence references | Cited file and field locations resolve in the inspected package |
| Actual tool invocations | Every validation request, including repeated requests |
| Elapsed time | Recorded duration for each run |
| Model tokens and cost | Reported input, output, and service charge |
| Guard interventions | How often fixed checks changed or constrained a recommendation |
| Repeat stability | Whether the same case receives the same recommendation across repeats |

A finding reference is more than a string. The evaluator must verify the referenced artifact and its field. Unknown evidence, malformed inputs, unavailable tools, unsupported findings, changed sources, and budget stops are meaningful failure scenarios.

## Spending control

The paid evaluation has a $5 total ceiling. Before each model request, reserve its maximum expected charge based on verified pricing and configured token limits. Stop if the next request could exceed the remaining budget or reliable cost information is unavailable. Record completed and failed requests with reported usage.

This control caps the planned study's service spending. The public website never sends a paid model request.

## What stays separate

The original harness study evaluates synthetic candidate modules. The 20 case pilot evaluates an earlier capstone configuration. The 40 case benchmark compares three workflows. Their case counts, timing, tools, and purposes differ. Results are displayed separately and tied to their recorded source files.

The study does not measure reviewer time, acquisition outcomes, lifecycle savings, operational security, or performance of a deployed defense system. These limits constrain the conclusions.
