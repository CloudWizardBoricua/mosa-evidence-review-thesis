# Understand the Terms

Use the site search for any term on this page. Each entry gives a meaning, an example, and a reason it matters. Colors organize topics; the written labels carry the meaning.

## Blue: evidence and checks

| Term | Meaning | Example | Why it matters |
| --- | --- | --- | --- |
| MOSA | Modular Open Systems Approach. Design systems so components can be inspected, replaced, and upgraded through defined connections. | Replace a processor without rewriting its neighboring components. | An openness claim needs evidence about how replacement works. |
| Component or module | A part of a system with a defined job. | A program that processes sensor readings. | It is the part reviewed or replaced in the examples. |
| Interface | A defined connection between components. | A service accepts a reading with a value and a unit. | Agreement about inputs and outputs makes components work together. |
| Interface contract | A precise statement of what an interface accepts and returns. | A required field named `event_id` must be preserved in output. | A checker needs a clear rule to detect disagreement. |
| Conformance | Meeting a stated set of rules. | A package provides every required field in the expected format. | Conformance describes the rules tested, not all possible qualities. |
| Harness | A program that runs checks and records the evidence. | The original thesis harness tests known faulty modules. | It makes repeated comparisons inspectable. |
| Validator | A tool that checks a specific rule. | Compare an interface version with the required version. | A tool result gives evidence for a recommendation. |
| Manifest | A machine readable description of a package. | A file lists the component name and interface version. | A missing description can make review incomplete. |
| SBOM | Software Bill of Materials. A list of the software components in a package. | A package lists a library and its version. | It helps identify undeclared or incompatible software. |
| Provenance | The record of where a file or result came from. | A release records its source commit and file hashes. | A reader can identify the exact material behind a claim. |
| Hash or digest | A calculated fingerprint of file contents. | A saved SHA-256 value changes when a source file changes. | It helps detect change and verify a copy. |
| SHA-256 | Secure Hash Algorithm with a 256 bit output. A commonly used file fingerprint calculation. | Compare a download with a recorded fingerprint. | It supports integrity checks without proving that the content is correct. |
| Schema | Rules for the shape and required fields of a record. | A result must contain a case identifier and disposition. | A well formed record can be read consistently. |
| JSON | JavaScript Object Notation. A structured text format. | A result contains `case_id`, `mode`, and `findings`. | It lets tools and the website read the same evidence. |

!!! info "Blue: a passing check has a boundary"
    A schema check can show that a record has the required fields. It cannot show that the claims inside those fields are true. The thesis states which rules each tool checks so the reader can see that boundary.

## Purple: agent decisions

| Term | Meaning | Example | Why it matters |
| --- | --- | --- | --- |
| Agent | A model that chooses an action from a permitted set. | Request an inventory check after inspecting a package. | Its choices can change review effort and coverage. |
| Bounded loop | A review process with limits on available actions and length. | Stop after the configured number of steps. | It limits repeated work and makes failures visible. |
| Model | A service that produces responses from instructions and input. | The configured OpenRouter model chooses the next check. | Model outputs can vary and need evidence checks. |
| LLM | Large Language Model. A model trained to process and produce language. | Draft a plain language explanation of a finding. | Fluency does not establish accuracy. |
| Prompt | The instructions and input supplied to a model. | Tell the model to use only the permitted tools. | Changing the prompt can change behavior. |
| Token | A unit used by a model to process text. | A request uses input tokens and produces output tokens. | Token use contributes to reported service cost. |
| Tool invocation | One request to run a validation tool. | Request the interface tool twice. | Two requests count as two invocations, even with one tool name. |
| Model request | One communication with the model service. | Ask the model to choose its next step. | This is different from a validation tool call. |
| OpenRouter | The hosted service used to reach the configured model. | Send a permitted tool selection request through the service. | Service access and reported pricing affect reproducibility. |

## Green, amber, and crimson: recommendations

| Term | Meaning | Example | Why it matters |
| --- | --- | --- | --- |
| Disposition | The review's recommendation category. | `ready`, `needs_review`, or `not_ready`. | It tells a person what decision the evidence currently supports. |
| Ready, green | Required checks support readiness within the research profile. | The supplied interface and inventory pass the required checks. | It is a limited result, not complete system certification. |
| Needs review, amber | Evidence or validation coverage is incomplete or unknown. | A required manifest is missing. | A person needs more information before deciding. |
| Not ready, crimson | A demonstrated blocking problem prevents readiness. | The stated interface version conflicts with the required version. | It calls for a specific correction. |
| Raw recommendation | The method's output before fixed decision checks. | A model recommends `not_ready` for missing evidence. | It exposes the method's own decision behavior. |
| Guarded recommendation | The recommendation allowed by the fixed guard. | The guard changes missing evidence to `needs_review`. | It shows how fixed checks affect reliability. |
| Decision guard | Fixed rules that require supported findings and sufficient checks. | Refuse readiness when a required tool was unavailable. | It prevents a persuasive explanation from bypassing evidence requirements. |
| Finding | A recorded issue with an evidence reference. | The interface version does not match the requirement. | It gives a reviewer something specific to inspect. |
| Remediation | The proposed correction for a finding. | Supply the missing inventory file. | It connects the issue to an actionable next step. |
| Approval | A recorded human decision in the private prototype. | A reviewer accepts a recommendation after inspecting its evidence. | A model recommendation does not replace responsibility. |
| Rollback | Restore an earlier recorded state. | Reverse an approved change after a review detects a problem. | It supports recovery while preserving the review history. |

!!! warning "Amber: unknown is a useful result"
    If evidence is missing, the correct result can be further review. Recording that uncertainty is more useful than inventing a definitive answer.

## Blue: study methods and measurement

| Term | Meaning | Example | Why it matters |
| --- | --- | --- | --- |
| Benchmark | A defined set of cases for comparing methods. | Forty synthetic packages with recorded expected answers. | It makes the comparison repeatable within that set. |
| Development cases | Cases used while building or adjusting the method. | Twenty packages inform implementation. | Performance on these cases may reflect development choices. |
| Additional evaluation cases | Cases reported in a separate comparison from development cases. | Twenty additional packages support the primary comparison. | Separate reporting and disclosure of preflight changes help readers assess bias. |
| Expected answer or label | The researcher's recorded correct outcome for a case. | A missing required record is labeled `needs_review`. | Accuracy depends on the quality and independence of labels. |
| Accuracy | The share of unique cases whose recommendation matches the expected answer. | Nineteen correct results out of twenty cases is 95 percent. | It measures agreement with labels, not universal correctness. |
| Missed finding | An expected issue that a review did not report. | A known interface conflict goes unreported. | It reveals a detection gap. |
| Extra finding | An issue reported without support in the expected evidence. | A review claims a missing field that is present. | It can cause unnecessary work or incorrect decisions. |
| Citation validity | Whether a reference points to the actual source and location, or establishes that a required location is absent. | The cited interface version exists, or the cited parent record shows a missing required field. | A nonempty citation string alone is insufficient. |
| Latency | Elapsed time for a review. | A hosted model review takes several seconds. | Less validation effort does not necessarily mean less time. |
| Median | The middle value after measurements are ordered. | The typical pilot review time is summarized by its median. | It is less affected by one unusually long run than an average. |
| Repeat | Another execution of the same case and method. | Run each method three times per case. | Repeats measure stability and timing, not new independent cases. |
| Synthetic | Created for research rather than collected from an operational system. | Deliberately omit a field in a test package. | Conclusions must stay within the example boundary. |
| MBSE | Model Based Systems Engineering. Use structured models to describe and reason about a system. | Connect a requirement to a system component model. | The earlier thesis covered it more broadly; this draft keeps only needed context. |

## Blue: repository and publication

| Term | Meaning | Example | Why it matters |
| --- | --- | --- | --- |
| Repository | A versioned collection of project files. | The thesis's GitHub repository. | Readers can inspect code, evidence, and changes together. |
| Commit | A recorded version of repository contents. | A tested capstone release records its commit identifier. | It identifies the exact source behind an evaluation. |
| Codespace | A hosted development environment. | The class project runs in its existing private workspace. | It runs code that the public reading site does not execute. |
| GitHub Pages | Hosting for generated static website files. | The committee reading site serves saved reports. | It supports public reading without a Python backend. |
| MkDocs Material | Tools that build a searchable documentation website from text files. | Build these pages from Markdown. | It keeps the reading site maintainable alongside the evidence. |
| Markdown | A text format for headings, tables, links, and other documentation. | This glossary is written in a `.md` file. | The source stays readable in GitHub. |
| Mermaid | A text syntax for drawing diagrams. | A flowchart describes the review sequence. | Diagrams can be versioned and reviewed with the documentation. |
| API | Application Programming Interface. A defined way for programs to communicate. | A private tool sends a model service request. | Public documentation should state which communications it depends on. |
| HTTP | Hypertext Transfer Protocol. Rules for web requests and responses. | Error 404 means the requested resource was not found. | A failed service request is an execution limit, not proof of model accuracy. |
| CLI | Command Line Interface. Commands typed into a terminal. | Run an offline verification command. | It supports repeatable checks beyond a visual interface. |
| CI | Continuous Integration. Automated checks run when repository changes are proposed. | Verify published files before a website deployment. | It helps catch broken evidence links and inconsistent results. |

Read [one saved review](review.md) to see these terms in use.
