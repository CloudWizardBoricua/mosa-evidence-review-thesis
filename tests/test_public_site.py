"""Check public evidence integrity and meaningful reading-site release boundaries."""
import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TITLE = "A CONFORMANCE HARNESS FOR VERIFIABLE MODULAR OPEN SYSTEMS OUTCOMES IN DEFENSE ACQUISITION: DESIGN, IMPLEMENTATION, AND CONTROLLED EVALUATION"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class PublicSiteTests(unittest.TestCase):
    def test_new_draft_keeps_original_title_and_reserves_author_rights(self):
        self.assertIn(TITLE, (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn(TITLE, (DOCS / "thesis.md").read_text(encoding="utf-8"))
        self.assertIn(TITLE, (ROOT / "CITATION.cff").read_text(encoding="utf-8"))
        self.assertIn("All rights reserved", (ROOT / "LICENSE").read_text(encoding="utf-8"))
        self.assertIn("conflicting", (ROOT / "LICENSE").read_text(encoding="utf-8"))

    def test_result_tables_equal_canonical_export(self):
        spec = importlib.util.spec_from_file_location("public_data", ROOT / "tools/render_public_data.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        content = module.render(read_json(DOCS / "assets/study_summary.json"))
        for path in (ROOT / "README.md", DOCS / "results.md"):
            with self.subTest(path=path.name):
                module.update(path, content, check=True)

    def test_summary_counts_use_unique_cases_and_valid_costs(self):
        summary = read_json(DOCS / "assets/study_summary.json")
        self.assertEqual(summary["schema_version"], 1)
        dataset_ids = [dataset["id"] for dataset in summary["datasets"]]
        self.assertEqual(len(set(dataset_ids)), len(dataset_ids))
        self.assertGreaterEqual(len(dataset_ids), 3, "Keep legacy, pilot, and new study evidence separate")
        for dataset in summary["datasets"]:
            for method in dataset.get("methods", []):
                with self.subTest(dataset=dataset["id"], mode=method["mode"]):
                    cases = method.get("cases")
                    for key in ("raw_correct", "guarded_correct"):
                        if method.get(key) is not None:
                            self.assertIsInstance(cases, int)
                            self.assertGreaterEqual(method[key], 0)
                            self.assertLessEqual(method[key], cases)
                    if method.get("cost_usd") is not None:
                        self.assertGreaterEqual(method["cost_usd"], 0)
                    if method.get("tool_invocations") is not None:
                        self.assertGreaterEqual(method["tool_invocations"], 0)
        budget = summary["budget"]
        self.assertEqual(budget["limit_usd"], 5)
        if budget.get("spent_usd") is not None:
            self.assertLessEqual(budget["spent_usd"], 5)

    def test_saved_reviews_have_traceable_identifiers_and_outcomes(self):
        saved = read_json(DOCS / "assets/reviews.json")
        self.assertEqual(saved["schema_version"], 1)
        self.assertTrue(saved["runs"])
        ids = [run["run_id"] for run in saved["runs"]]
        self.assertEqual(len(set(ids)), len(ids))
        outcomes = {"ready", "needs_review", "not_ready"}
        for run in saved["runs"]:
            with self.subTest(run_id=run["run_id"]):
                self.assertTrue(run["case_id"])
                self.assertTrue(run["mode"])
                self.assertTrue(run["split"])
                self.assertIsInstance(run["repeat"], int)
                if run["raw_disposition"] is None:
                    self.assertEqual(run["status"], "failed")
                    self.assertEqual(run["mode"], "openrouter")
                else:
                    self.assertIn(run["raw_disposition"], outcomes)
                self.assertIn(run["guarded_disposition"], outcomes)
                for finding in run.get("findings", []):
                    self.assertTrue(finding["id"])
                    if finding.get("citation_valid") is True:
                        self.assertTrue(finding.get("artifact"))
                        self.assertTrue(finding.get("field"))
                for source in run.get("sources", []):
                    self.assertTrue(source["artifact"])
                    url = urlparse(source["url"])
                    self.assertNotIn(url.scheme, {"javascript", "data", "file"})
                    prefix = "/CloudWizardBoricua/mosa-evidence-review-thesis/blob/main/"
                    if url.hostname == "github.com" and url.path.startswith(prefix):
                        local = ROOT / unquote(url.path[len(prefix):])
                        self.assertTrue(local.resolve().is_relative_to(ROOT.resolve()))
                        self.assertTrue(local.is_file(), f"Saved source reference does not exist: {source['url']}")
                if run["split"] in {"development", "heldout"}:
                    invocations = sum(event.get("type") == "tool" for event in run.get("events", []))
                    self.assertEqual(run["metrics"]["tool_invocations"], invocations)

    def test_documentation_links_and_image_fallbacks_exist(self):
        for path in [ROOT / "README.md", *DOCS.glob("*.md")]:
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
                target = target.split(" ", 1)[0].strip("<>")
                parsed = urlparse(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                local = path.parent / unquote(parsed.path)
                with self.subTest(source=path.name, target=target):
                    self.assertTrue(local.exists(), f"Missing local reader reference: {target}")
        for stem in ("system_topology", "review_sequence", "approval_rollback", "migration"):
            for suffix in ("svg", "png"):
                self.assertTrue((DOCS / "assets/diagrams" / f"{stem}.{suffix}").is_file())
            self.assertTrue((ROOT / "diagrams" / f"{stem}.mmd").is_file())

    def test_diagram_text_and_sources_agree(self):
        blocks = re.findall(r"```mermaid\n(.*?)```", (DOCS / "diagrams.md").read_text(encoding="utf-8"), re.S)
        stems = ("system_topology", "review_sequence", "approval_rollback", "migration")
        self.assertEqual(len(blocks), len(stems))
        for stem, block in zip(stems, blocks):
            with self.subTest(diagram=stem):
                source = (ROOT / "diagrams" / f"{stem}.mmd").read_text(encoding="utf-8")
                self.assertEqual(source.strip(), block.strip())
                self.assertIn("classDef evidence", source)
        readme_block = re.search(r"```mermaid\n(.*?)```", (ROOT / "README.md").read_text(encoding="utf-8"), re.S)
        self.assertEqual(readme_block.group(1).strip(), blocks[0].strip())

    def test_new_prose_avoids_long_dash_characters(self):
        for path in [ROOT / "README.md", *DOCS.glob("*.md")]:
            with self.subTest(path=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("\u2014", content)
                self.assertNotIn("\u2013", content)

    def test_public_exports_exclude_private_application_state_and_secrets(self):
        paths = list(DOCS.rglob("*.json")) + list((ROOT / "evidence/pilot").glob("*.json"))
        bad_key = re.compile(r'"(?:api_key|authorization|access_token|review_state|current_approval|approval_history)"\s*:', re.I)
        secret_value = re.compile(r"sk-(?:or-v1-)?[A-Za-z0-9]{24,}|gh[pousr]_[A-Za-z0-9]{24,}")
        temporary_host = re.compile(r"https?://[^\s\"]*app\.github\.dev|animated-space-goldfish", re.I)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                content = path.read_text(encoding="utf-8")
                self.assertIsNone(bad_key.search(content))
                self.assertIsNone(secret_value.search(content))
                self.assertIsNone(temporary_host.search(content))
        self.assertFalse((DOCS / "review_state.json").exists())
        if (ROOT / "prototypes/capstone").exists():
            manifest = read_json(ROOT / "prototypes/capstone/MIGRATION.json")
            for field in ("source_repository", "source_commit", "files", "verification", "migration_date"):
                self.assertTrue(manifest[field], "Public capstone code requires a completed tested migration record")

    def test_unexecuted_model_results_are_not_displayed_as_zero_accuracy(self):
        spec = importlib.util.spec_from_file_location("public_data", ROOT / "tools/render_public_data.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        pending = {"schema_version": 1, "datasets": [{"id": "pending", "cases": 20, "runs": 0, "methods": [{"mode": "openrouter", "cases": 20, "runs": 0, "raw_correct": 0, "guarded_correct": 0, "tool_invocations": 0, "cost_usd": None}]}]}
        text = module.render(pending)
        self.assertIn("Not executed", text)
        self.assertNotIn("0/20", text)

    def test_pilot_tables_retain_source_measurements(self):
        fixed = read_json(ROOT / "evidence/pilot/baseline_summary.json")
        model = read_json(ROOT / "evidence/pilot/openrouter_summary.json")
        summary = read_json(DOCS / "assets/study_summary.json")
        pilots = [dataset for dataset in summary["datasets"] if dataset["id"] == "pilot"]
        self.assertEqual(len(pilots), 1)
        methods = {method["mode"]: method for method in pilots[0]["methods"]}
        for name, source in (("baseline", fixed), ("openrouter", model)):
            method = methods[name]
            self.assertEqual(method["cases"], source["cases"])
            self.assertEqual(method["raw_correct"], source["raw_disposition_correct"])
            self.assertEqual(method["guarded_correct"], source["disposition_correct"])
            self.assertEqual(method["tool_invocations"], source["total_tool_calls"])
            self.assertEqual(method["median_elapsed_ms"], source["median_latency_ms"])

    def test_website_dependencies_and_actions_are_pinned(self):
        requirements = (ROOT / "requirements-site.txt").read_text(encoding="utf-8")
        for line in requirements.splitlines():
            if line and not line.startswith("#"):
                self.assertRegex(line, r"^[A-Za-z0-9_.-]+==[^\s]+$")
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        for action in re.findall(r"uses:\s*(\S+)", workflow):
            self.assertRegex(action, r"^[A-Za-z0-9_./-]+@[0-9a-f]{40}$")
        self.assertIn("mkdocs build --strict", workflow)
        self.assertIn("render_public_data.py --check", workflow)


if __name__ == "__main__":
    unittest.main()
