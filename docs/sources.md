# Sources and Rights

This public companion connects claims to source files, recorded runs, and references. The author retains rights. Public access does not imply committee approval or a general reuse license.

## Source records

| Dataset | Recorded source | What it supports |
| --- | --- | --- |
| Original harness study | [Statistical summary](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/evidence/legacy/statistical_summary.json) and [preserved prototype](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/tree/main/prototypes/legacy-harness) | Known fault detection and original timing |
| Capstone pilot | [Fixed summary](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/evidence/pilot/baseline_summary.json), [model summary](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/evidence/pilot/openrouter_summary.json), and [sanitized analysis](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/evidence/pilot/hosted_analysis.json) | Pilot decisions, tool counts, timing, and reported model charges |
| New benchmark | [Public verified summary](assets/study_summary.json) and [saved reviews](assets/reviews.json) | Only executed, recorded comparisons described in the export |

The pilot source records do not validate each original citation against an actual file and field. The new comparison requires that stronger check. An unavailable source reference is a recorded limit and must not be invented.

Provenance means the record of where an artifact came from. Source commit identifiers, frozen settings, file hashes, and run identifiers let another reader locate the same evidence. SHA-256 is the file fingerprint calculation used by the project.

## Author rights and inherited notices

The [repository license notice](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/LICENSE) reserves the author's rights in new work. The inherited harness retains its [original notice](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/prototypes/legacy-harness/LICENSE.txt) and [citation metadata](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/prototypes/legacy-harness/CITATION.cff).

Those inherited files conflict: the notice subjects reuse to author and university approval, while the citation metadata lists MIT. The MIT label is not adopted as a repository wide license. This companion preserves the record and does not resolve the conflict or relicense the source.

Use [the new citation file](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/CITATION.cff) for this companion. Identify the revised draft and dataset version used. Third party packages retain their own licenses.

## Official publication and formatting references

The website uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/getting-started/) and [GitHub's Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Build dependencies and deployment actions are pinned to specific versions.

Diagrams use [GitHub supported Mermaid syntax](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams). Matching image exports make them available to readers who cannot render the diagram text.

The revised thesis follows [the University of Oklahoma thesis formatting instructions](https://www.ou.edu/content/dam/gradcollege/docs/gc-thesis-dissertation-instruction-packet.pdf). The crimson accent follows [OU's color reference](https://www.ou.edu/brand/creative-platform/design-system/colors). Visual branding does not imply approval.
