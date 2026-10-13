# Start Here

<div class="hero" markdown="1">

<span class="eyebrow">A research draft for committee review</span>

## Can an agent make evidence review more useful?

The thesis asks when an agent helps a person review evidence for the Modular Open Systems Approach, and which fixed checks keep its recommendations reliable.

[Read the thesis](thesis.md){ .md-button .md-button--primary }
[Follow one review](review.md){ .md-button }

</div>

The Modular Open Systems Approach, or **MOSA**, means designing a system so components can be inspected, replaced, and upgraded through clearly defined connections. The research uses synthetic software examples to ask whether the evidence supports those claims.

An agent is a model that selects its next action from a permitted set. Here it can request checks and draft a recommendation. A person remains responsible for review and approval.

!!! info "Blue: what counts as evidence?"
    Evidence is a record that can support or challenge a claim. Examples include an interface description, a list of software components, and a record of where files came from. An explanation is useful only when a reader can trace it to those records.

## The reading path

| Step | Read this | Purpose |
| --- | --- | --- |
| 1 | This page | Understand the question and the boundary |
| 2 | [Read the Thesis](thesis.md) | Find the revised source, chapter guide, and download status |
| 3 | [Follow One Review](review.md) | Inspect a saved recommendation and its evidence |
| 4 | [Compare Results](results.md) | Compare methods without mixing datasets |
| 5 | [Understand the Terms](glossary.md) | Find plain language definitions and examples |
| 6 | [Reproduce the Study](reproduce.md) | Verify results and repeat supported checks |

## Three layers of the contribution

<div class="reading-grid" markdown="1">

<div class="reading-card evidence" markdown="1">
### Blue: fixed checks
The original harness shows how explicit rules detect known faults. A harness is a program that runs a set of tests and records the results.
</div>

<div class="reading-card agent" markdown="1">
### Purple: agent choices
The capstone adds a bounded agent that selects checks. Bounded means its tools, actions, and review length have explicit limits.
</div>

<div class="reading-card review" markdown="1">
### Amber: responsible review
The guard requires evidence and completed checks. A person reviews the resulting recommendation before any private prototype action.
</div>

</div>

## What this resource can establish

The recorded studies show behavior within specific synthetic examples. They can demonstrate whether checks detected a known issue, whether a recommendation cited evidence, and how much recorded effort a review required. They cannot establish defense program certification, field performance, procurement approval, or lifecycle savings.

The revised draft keeps the earlier thesis's exact title. Its contents are a new, shorter research draft with a capstone evaluation. The original document remains unchanged. [See what was kept and shortened](changes.md).

## Color and word labels

| Label | Meaning |
| --- | --- |
| <span class="legend evidence">Blue: evidence and fixed checks</span> | Records and tests with explicit rules |
| <span class="legend agent">Purple: agent choices</span> | Permitted model decisions |
| <span class="legend ready">Green: ready</span> | Required checks support readiness within the profile |
| <span class="legend review">Amber: further review</span> | Evidence or coverage is missing or unknown |
| <span class="legend blocked">Crimson: blocking problem</span> | A known problem prevents readiness |

Every visual uses words as well as colors. Use the site search to find an acronym or topic.
