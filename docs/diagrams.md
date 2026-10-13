# System Diagrams

The diagrams show how the evidence moves through the review process. Each diagram has an image export and text source. Color labels distinguish evidence, model choices, uncertainty, and supported readiness.

## System topology

Topology means the arrangement of parts and connections. The three methods share the same validators and decision guard.

Fixed checks run every validator. Rule choices use explicit rules. Model choices come from the bounded agent. The shared tools inspect evidence, compare interfaces, and check the software inventory. The fixed guard checks coverage and support before the saved report reaches a person or the public reading record.

```mermaid
flowchart TB
    Evidence["Evidence"]:::evidence
    Fixed["Fixed checks"]:::evidence
    Rules["Rule choices"]:::evidence
    Agent["Model choices"]:::agent
    Tools["Shared tools"]:::evidence
    Guard["Fixed guard"]:::evidence
    Report["Saved report"]:::evidence
    Human["Human review"]:::review
    Archive["Public record"]:::evidence
    Evidence --> Fixed & Rules & Agent
    Fixed & Rules & Agent --> Tools
    Tools --> Guard
    Guard --> Report
    Report --> Human
    Report --> Archive
    classDef evidence fill:#e8f1fb,stroke:#1565c0,color:#102f53
    classDef agent fill:#f0e6fa,stroke:#6a1b9a,color:#431263
    classDef review fill:#fff2d4,stroke:#9a6200,color:#563600
    classDef ready fill:#e4f3e8,stroke:#24713a,color:#164724
```

![System topology with shared validators, a decision guard, and human review](assets/diagrams/system_topology.svg)

## Review sequence

The method can request a tool, inspect the returned facts, and choose another permitted action. Every request is counted. Another check is allowed only when needed and within the loop limit. A raw report records the method's recommendation before the fixed guard. The guard then returns ready, further review, or not ready, with evidence references.

```mermaid
flowchart TD
    Start["Read evidence"]:::evidence
    Choose["Choose check"]:::agent
    Check["Tool result"]:::evidence
    More["Another check?"]:::review
    Draft["Raw report"]:::agent
    Guard["Fixed guard"]:::evidence
    Ready["Ready"]:::ready
    Review["Further review"]:::review
    Blocked["Not ready"]:::blocked
    Start --> Choose --> Check --> More
    More -->|Yes| Choose
    More -->|No| Draft --> Guard
    Guard --> Ready & Review & Blocked
    classDef evidence fill:#e8f1fb,stroke:#1565c0,color:#102f53
    classDef agent fill:#f0e6fa,stroke:#6a1b9a,color:#431263
    classDef review fill:#fff2d4,stroke:#9a6200,color:#563600
    classDef ready fill:#e4f3e8,stroke:#24713a,color:#164724
    classDef blocked fill:#f8e8ea,stroke:#841617,color:#641113
```

![Review sequence from evidence to guarded recommendation](assets/diagrams/review_sequence.svg)

## Approval and rollback

This diagram describes private prototype behavior. A person reviews evidence, the source fingerprint must match, and history remains available after rollback. A changed source requires another review. Restore prior means restore the previous approved pointer and append a history entry. Keep current means retain the current pointer and its recorded history.

```mermaid
flowchart TD
    Saved["Saved report"]:::evidence
    Person["Human review"]:::review
    Changed["Source changed?"]:::review
    Rerun["Review again"]:::blocked
    Approved["Record approval"]:::evidence
    Later["Rollback?"]:::review
    Restore["Restore prior"]:::evidence
    Keep["Keep current"]:::evidence
    Saved --> Person --> Changed
    Changed -->|Yes| Rerun
    Changed -->|No, approved| Approved --> Later
    Later -->|Yes| Restore
    Later -->|No| Keep
    classDef evidence fill:#e8f1fb,stroke:#1565c0,color:#102f53
    classDef review fill:#fff2d4,stroke:#9a6200,color:#563600
    classDef ready fill:#e4f3e8,stroke:#24713a,color:#164724
    classDef blocked fill:#f8e8ea,stroke:#841617,color:#641113
```

![Private approval checks source changes and preserves history during rollback](assets/diagrams/approval_rollback.svg)

## Migration after course submission

The class project stays in place after course submission. A checked archive contains a tested release, source commit, and file hashes. Its contents are copied into the thesis repository. Fresh tests run from a new independent checkout. The thesis copy then supports future work, while the original class history remains available.

```mermaid
flowchart TD
    Class["Class project"]:::evidence
    Tested["Tested release"]:::evidence
    Export["Checked archive"]:::review
    Thesis["Thesis copy"]:::evidence
    Fresh["Fresh tests"]:::evidence
    Main["Future work"]:::evidence
    Class --> Tested --> Export --> Thesis --> Fresh --> Main
    Class --> Preserved["History kept"]:::evidence
    classDef evidence fill:#e8f1fb,stroke:#1565c0,color:#102f53
    classDef review fill:#fff2d4,stroke:#9a6200,color:#563600
    classDef ready fill:#e4f3e8,stroke:#24713a,color:#164724
```

![Migration copies a tested release and preserves class history](assets/diagrams/migration.svg)

## Diagram sources and fallback files

| Diagram | Editable source | PNG fallback |
| --- | --- | --- |
| System topology | [Mermaid source](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/diagrams/system_topology.mmd) | [PNG image](assets/diagrams/system_topology.png) |
| Review sequence | [Mermaid source](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/diagrams/review_sequence.mmd) | [PNG image](assets/diagrams/review_sequence.png) |
| Approval and rollback | [Mermaid source](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/diagrams/approval_rollback.mmd) | [PNG image](assets/diagrams/approval_rollback.png) |
| Migration | [Mermaid source](https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/diagrams/migration.mmd) | [PNG image](assets/diagrams/migration.png) |

SVG means Scalable Vector Graphics. These images remain sharp when enlarged. PNG means Portable Network Graphics, a widely supported image format. Mermaid is the editable text description from which the diagrams are produced.
