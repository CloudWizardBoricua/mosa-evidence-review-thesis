"""Build public result tables from the canonical summary, without model calls."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- BEGIN VERIFIED RESULTS -->"
END = "<!-- END VERIFIED RESULTS -->"


def number(value, digits=0):
    if value is None:
        return "Not reported"
    return f"{value:,.{digits}f}".rstrip("0").rstrip(".") if digits else f"{value:,}"


def clean(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ").replace("\u2014", ", ").replace("\u2013", " to ")


def correct(value, cases):
    if value is None or not cases:
        return "Not reported"
    return f"{value}/{cases} ({100 * value / cases:.1f}%)"


def dataset_label(dataset):
    if dataset["id"] == "study40-heldout":
        return "New benchmark: additional-case evaluation"
    if dataset["id"] == "study40-development":
        return "New benchmark: development cases"
    return dataset.get("label", dataset["id"])


def render(summary):
    if summary.get("schema_version") != 1:
        raise ValueError("Unsupported summary schema_version")
    lines = []
    for dataset in summary["datasets"]:
        lines.extend([f"### {clean(dataset_label(dataset))}", "", f"**Status:** {clean(dataset.get('status', 'recorded'))}. Unique cases: {number(dataset.get('cases'))}. Recorded runs: {number(dataset.get('runs'))}.", ""])
        methods = dataset.get("methods", [])
        if methods and any("faults_detected" in method for method in methods):
            lines.extend(["| Method | Known faults detected | Controls accepted | Median elapsed time, ms |", "| --- | ---: | ---: | ---: |"])
            for method in methods:
                lines.append(f"| {clean(method.get('label', method['mode']))} | {method.get('faults_detected', 'Not reported')}/{method.get('faults', 'Not reported')} | {method.get('controls_accepted', 'Not reported')}/{method.get('controls', 'Not reported')} | {number(method.get('median_elapsed_ms'), 3)} |")
        elif methods:
            lines.extend(["| Method | Unique cases | Recorded runs | Raw correct | Guarded correct | Tool invocations | Median elapsed time, ms | Recorded cost, USD |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"])
            for method in methods:
                cases = method.get("cases")
                executed = method.get("runs", 0) > 0
                raw = correct(method.get('raw_correct'), cases) if executed else "Not executed"
                guarded = correct(method.get('guarded_correct'), cases) if executed else "Not executed"
                calls = number(method.get('tool_invocations')) if executed else "Not executed"
                lines.append(f"| {clean(method.get('label', method['mode']))} | {number(cases)} | {number(method.get('runs'))} | {raw} | {guarded} | {calls} | {number(method.get('median_elapsed_ms'), 3)} | {number(method.get('cost_usd'), 6)} |")
            for method in methods:
                if method.get("status") in {"incomplete", "pending"}:
                    lines.extend(["", f"**{clean(method.get('label', method['mode']))}: {method['status']}.** {number(method.get('runs'))} of {number(method.get('planned_runs'))} planned runs recorded; {number(method.get('timed_runs'))} completed reviews with timing; {number(method.get('failed_runs'))} failed runs. A complete recommendation accuracy comparison is not available."])
            if any(method.get("reference_count") is not None for method in methods):
                lines.extend(["", "| Method | Missed findings | Extra findings | Valid references | Guard interventions | Fully repeated stable cases | Tokens |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"])
                for method in methods:
                    if not method.get("runs", 0):
                        lines.append(f"| {clean(method.get('label', method['mode']))} | Not executed | Not executed | Not executed | Not executed | Not executed | Not executed |")
                        continue
                    refs = f"{method.get('valid_reference_count', 'Not reported')}/{method.get('reference_count', 'Not reported')}"
                    stable = f"{method.get('stable_cases', 'Not reported')}/{method.get('fully_repeated_cases', 'Not reported')}"
                    tokens = None if method['mode'] == 'openrouter' and method.get('timed_runs') == 0 else method.get('tokens')
                    lines.append(f"| {clean(method.get('label', method['mode']))} | {number(method.get('missed_findings'))} | {number(method.get('extra_findings'))} | {refs} | {number(method.get('guard_interventions'))} | {stable} | {number(tokens)} |")
                lines.extend(["", "Findings, references, and guard interventions count recorded runs. Stable case counts require all planned repeats. These counts use a different denominator from unique-case recommendation accuracy."])
        else:
            lines.append("No executed method results are available for this dataset.")
        lines.append("")
        for note in dataset.get("notes", []):
            lines.extend([clean(note), ""])
        if dataset.get("source_url"):
            lines.extend([f"[Inspect the recorded source]({dataset['source_url']}).", ""])
    budget = summary.get("budget")
    if budget:
        spent = "Not reported" if budget.get("spent_usd") is None else "$" + number(budget["spent_usd"], 6)
        lines.extend([f"**New study budget:** ${number(budget.get('limit_usd'), 2)} ceiling; recorded spending: {spent}. Unknown cost is never treated as zero.", ""])
        if budget.get("stop_reason"):
            lines.extend([f"**Paid study stopped:** {clean(budget['stop_reason'])}.", ""])
    lines.append("Accuracy counts unique cases. Repeated runs measure stability and timing. Pilot invocation counts retain the original evaluator's definition; the new benchmark counts actual trace events.")
    return "\n".join(lines).strip()


def update(path, content, check=False):
    source = path.read_text(encoding="utf-8")
    if source.count(BEGIN) != 1 or source.count(END) != 1:
        raise ValueError(f"Missing or duplicate result markers in {path.name}")
    left, remainder = source.split(BEGIN)
    _, right = remainder.split(END)
    revised = left + BEGIN + "\n" + content + "\n" + END + right
    if revised == source:
        return
    if check:
        raise ValueError(f"Generated results are stale in {path.name}; run tools/render_public_data.py")
    path.write_text(revised, encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the checked in tables differ from the verified export")
    args = parser.parse_args()
    summary = json.loads((ROOT / "docs/assets/study_summary.json").read_text(encoding="utf-8"))
    content = render(summary)
    for path in (ROOT / "README.md", ROOT / "docs/results.md"):
        update(path, content, args.check)
    print("Verified result tables are current." if args.check else "Rendered verified tables in README and website.")


if __name__ == "__main__":
    main()
