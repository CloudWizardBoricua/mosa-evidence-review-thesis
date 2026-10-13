"""Keep the reader's Mermaid text identical to the editable diagram sources."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEMS = ("system_topology", "review_sequence", "approval_rollback", "migration")


def main():
    blocks = [(ROOT / "diagrams" / f"{stem}.mmd").read_text(encoding="utf-8").strip() for stem in STEMS]
    for path, replacements in ((ROOT / "docs/diagrams.md", blocks), (ROOT / "README.md", blocks)):
        text = path.read_text(encoding="utf-8")
        matches = list(re.finditer(r"```mermaid\n.*?```", text, re.S))
        if len(matches) != len(replacements):
            raise ValueError(f"Unexpected Mermaid block count in {path.name}")
        for match, block in reversed(list(zip(matches, replacements))):
            text = text[:match.start()] + "```mermaid\n" + block + "\n```" + text[match.end():]
        path.write_text(text, encoding="utf-8", newline="\n")
    print("Mermaid reader blocks match the diagram sources.")


if __name__ == "__main__":
    main()
