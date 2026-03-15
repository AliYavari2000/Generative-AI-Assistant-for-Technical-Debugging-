
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("This script requires PyYAML. Install it with: pip install pyyaml") from exc


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


@dataclass
class FaultCard:
    id: str
    fault_name: str
    aliases: list[str]
    category: str
    bearing_components: list[str]
    observability_from_vibration: str
    confidence: str
    tags: list[str]
    references: list[dict[str, Any]]
    symptoms: list[str]
    likely_causes: list[str]
    expected_vibration_signatures: list[str]
    confirm_tests: list[str]
    fixes: list[str]
    notes: str
    source_file: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Missing or invalid YAML front matter")
    raw_yaml, body = match.groups()
    metadata = yaml.safe_load(raw_yaml) or {}
    return metadata, body.strip()


def extract_section(body: str, title: str) -> str:
    pattern = rf"##\s+{re.escape(title)}\s*\n(.*?)(?=\n##\s+|\Z)"
    match = re.search(pattern, body, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_bullets(section_text: str) -> list[str]:
    items = []
    for line in section_text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def parse_fault_card(path: Path) -> FaultCard:
    metadata, body = split_frontmatter(read_text(path))

    card = FaultCard(
        id=str(metadata.get("id", "")),
        fault_name=str(metadata.get("fault_name", "")),
        aliases=list(metadata.get("aliases", []) or []),
        category=str(metadata.get("category", "")),
        bearing_components=list(metadata.get("bearing_components", []) or []),
        observability_from_vibration=str(metadata.get("observability_from_vibration", "")),
        confidence=str(metadata.get("confidence", "")),
        tags=list(metadata.get("tags", []) or []),
        references=list(metadata.get("references", []) or []),
        symptoms=parse_bullets(extract_section(body, "Symptoms")),
        likely_causes=parse_bullets(extract_section(body, "Likely causes")),
        expected_vibration_signatures=parse_bullets(extract_section(body, "Expected vibration signatures")),
        confirm_tests=parse_bullets(extract_section(body, "Confirm tests")),
        fixes=parse_bullets(extract_section(body, "Fixes")),
        notes=extract_section(body, "Notes"),
        source_file=path.name,
    )
    return card


def index_row(card: FaultCard) -> dict[str, Any]:
    return {
        "id": card.id,
        "fault_name": card.fault_name,
        "category": card.category,
        "observability_from_vibration": card.observability_from_vibration,
        "confidence": card.confidence,
        "bearing_components": "|".join(card.bearing_components),
        "aliases": "|".join(card.aliases),
        "tags": "|".join(card.tags),
        "n_symptoms": len(card.symptoms),
        "n_causes": len(card.likely_causes),
        "n_signatures": len(card.expected_vibration_signatures),
        "n_confirm_tests": len(card.confirm_tests),
        "n_fixes": len(card.fixes),
        "n_references": len(card.references),
        "source_file": card.source_file,
    }


def write_json(path: Path, cards: list[FaultCard]) -> None:
    payload = [asdict(card) for card in cards]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, cards: list[FaultCard]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for card in cards:
            f.write(json.dumps(asdict(card), ensure_ascii=False) + "\n")


def write_csv(path: Path, cards: list[FaultCard]) -> None:
    rows = [index_row(card) for card in cards]
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse bearing fault cards from Markdown to JSON/JSONL/CSV")
    parser.add_argument("--input_dir", type=Path, default=Path("fault_cards"))
    parser.add_argument("--out_dir", type=Path, default=Path("exports"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(args.input_dir.glob("*.md"))
    if not paths:
        raise SystemExit(f"No Markdown files found in {args.input_dir}")

    cards = [parse_fault_card(path) for path in paths]

    write_json(args.out_dir / "fault_cards.json", cards)
    write_jsonl(args.out_dir / "fault_cards.jsonl", cards)
    write_csv(args.out_dir / "fault_cards_index.csv", cards)

    print(f"Parsed {len(cards)} cards.")
    print(f"Wrote: {args.out_dir / 'fault_cards.json'}")
    print(f"Wrote: {args.out_dir / 'fault_cards.jsonl'}")
    print(f"Wrote: {args.out_dir / 'fault_cards_index.csv'}")


if __name__ == "__main__":
    main()
