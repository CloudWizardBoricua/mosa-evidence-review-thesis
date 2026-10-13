# Follow One Review

A review has five parts: what was checked, what was found, why it matters, what to correct, and what remains unknown. Select a case and method below to inspect a saved run.

<div id="review-explorer" class="interactive-panel" data-review-explorer>
<p role="status">Loading saved review records.</p>
</div>

<noscript><p>JavaScript is needed for the filters. <a href="../assets/reviews.json">Download the same saved review records</a> or read the walkthrough below.</p></noscript>

[Download the saved review data](assets/reviews.json). These are sanitized study records. The page cannot execute a review, approve a decision, or change any source file.

## How to read a recommendation

| Part | Question to ask |
| --- | --- |
| Checks | Which tools completed, and which could not run? |
| Raw recommendation | What did the method recommend before the fixed guard? |
| Guarded recommendation | What did the fixed decision checks allow? |
| Findings and references | Does each issue identify a source file and field? |
| Correction | What specific action would address the issue? |
| Unknowns | What evidence or check is still missing? |

!!! example "Purple: an agent choice"
    The model can request an inventory check after inspecting the evidence package. The inventory is the list of software components. The choice tells us what the agent tried to learn. The tool result tells us what was actually found.

!!! warning "Amber: missing evidence needs further review"
    In the recorded pilot, the model described three missing records as a blocking decision. The guard changed those recommendations to further review. Missing information and a demonstrated incompatibility mean different things, so the distinction affects the next action.

## One example from the pilot

The recorded pilot includes a package without a manifest. A manifest is a short machine readable description of the package. The model recommended `not_ready`. The fixed guard returned `needs_review`. This correction kept a missing record distinct from a proven incompatibility.

The pilot's saved evaluator records establish the raw and guarded decisions. They do not supply validated file and field references for every finding. The explorer identifies that evidence limit when displaying a pilot record. The new benchmark requires references that resolve to the cited file and field.

## Approval stays with a person

In the private prototype, a reviewer sees the recommendation and the evidence before approving it. The prototype checks whether source files changed since review. If they changed, the recommendation must be reviewed again. Rollback restores an earlier approved state and records what happened.

These are private prototype actions. The public site contains a record for reading and comparison. [See the approval and rollback diagram](diagrams.md#approval-and-rollback).
