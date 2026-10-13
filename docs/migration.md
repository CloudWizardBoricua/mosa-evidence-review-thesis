# Migration Guide

**Status: future transfer after course submission.** The class capstone remains in its existing repository. This guide copies a tested release into the thesis repository without moving or deleting the class history.

## Prepare the release

In the class Codespace, run the complete offline tests and controlled evaluation. Review the source files intended for transfer. Exclude credentials, private approval state, temporary service addresses, unrelated coursework, cached files, and development environments.

Commit the tested capstone release in the class repository. Record the commit identifier, model and prompt settings, label review status, evaluation commands, and cost ledger. A cost ledger records actual and reserved spending. Do not invent independent review or successful execution.

## Export an explicit set of files

Run from the class repository root after the release is committed:

```bash
git rev-parse HEAD
git status --short
git ls-tree -r --name-only HEAD capstone
```

The first command identifies the source version. The second shows uncommitted changes. The third lists the versioned capstone files. Inspect that list before archiving. Include only the source, tests, synthetic fixtures, frozen study settings, and sanitized evidence that are ready for publication.

Create the release archive from the explicit tested commit and an allowed list of paths. Run this command in the Linux class Codespace:

```bash
git archive --format=zip --output=mosa-capstone-release.zip HEAD \
  capstone/mosa_review.py capstone/server.py capstone/evaluate.py \
  capstone/generate_fixtures.py capstone/generate_study40.py \
  capstone/study40.py capstone/study_budget.py capstone/study_metrics.py \
  capstone/tests capstone/fixtures capstone/web \
  capstone/study40/packages capstone/study40/labels.json \
  capstone/study40/settings.json capstone/study40/freeze.json \
  capstone/study40/system_prompt.txt capstone/STUDY_PROTOCOL.md \
  capstone/README.md capstone/.gitignore
```

An archive is a copy of the selected committed files. It preserves the source snapshot without transferring unrelated class history. Its allowed paths exclude runtime approvals, remote credentials, preflight outputs, and budget state. Preserve the final sanitized results separately in the thesis evidence folder. If the tested release adds a required source file, document and review that addition to the allowed list before export.

Record a SHA-256 fingerprint for the archive and each exported file. SHA-256 is the file fingerprint algorithm. Confirm that protected source records have not changed.

## Integrate into the thesis repository

Extract the approved archive into `prototypes/capstone/` in a separate thesis branch. The archive contains a `capstone/` directory; place its contents at the new folder root so there is no duplicated `capstone/capstone/` nesting.

Update path references as one reviewed relocation change. Preserve fixture and recorded result bytes. Keep live credentials outside the repository. Include a `MIGRATION.json` record with these fields:

| Field | Meaning |
| --- | --- |
| `source_repository` | The class repository address |
| `source_commit` | The exact tested class commit |
| `source_directory` | `capstone` |
| `destination_directory` | `prototypes/capstone` |
| `archive_sha256` | The fingerprint of the exported archive |
| `files` | Source path, destination path, and SHA-256 for each transferred file |
| `evaluation_configuration` | The frozen settings file and its hash |
| `verification` | Exact fresh checkout commands and recorded outcomes |
| `migration_date` | The actual date the transfer is performed |

Do not fill these fields with example results. Record the real transfer when it occurs. Preserve inherited license and citation notices with the copied release.

## Verify an independent checkout

Clone the thesis repository into a fresh directory after the relocation branch is ready. Run the capstone tests using its relocated paths:

```bash
python -m unittest discover -s prototypes/capstone/tests -v
python prototypes/capstone/mosa_review.py review 03_interface_version --mode baseline
python prototypes/capstone/mosa_review.py review 03_interface_version --mode adaptive
```

Compare fixture hashes and frozen evaluation settings with the release manifest. Verify saved logical outcomes without requiring timing equality. Check that the prototype no longer depends on the class folder. Build the public website and inspect its links.

After this verification, merge the reviewed relocation change and mark the thesis repository as the source for future thesis development. Add a pointer in the class project documentation when the author is ready. Keep the class repository and its submitted history intact.

!!! warning "Amber: approval state is private"
    A saved public recommendation is research evidence. A person's current approval pointer and private notes are application state. They are excluded from the public release so the reading site cannot be mistaken for a live approval service.

![Migration from tested class release to independently verified thesis checkout](assets/diagrams/migration.svg)
