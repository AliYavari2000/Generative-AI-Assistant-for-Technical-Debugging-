"""
Parser for bearing-fault knowledge-base cards.

Supports two on-disk formats:
  A) YAML front matter  (bearing_fault_kb_starter style)
  B) Markdown table      (hand-authored fault_cards/ style)

Both are normalised into a single `FaultCard` Pydantic model so the rest of
the application never cares which format was used.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class Reference(BaseModel):
    title: str = ""
    source: str = ""
    url: str = ""


class FaultCard(BaseModel):
    id: str = Field(description="Unique identifier, e.g. BRG-001")
    fault_name: str = Field(description="Human-readable fault name")
    aliases: list[str] = Field(default_factory=list)
    category: str = ""
    bearing_components: list[str] = Field(default_factory=list)
    observability_from_vibration: str = ""
    diagnostic_confidence: str = ""
    tags: list[str] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)

    symptoms: list[str] = Field(default_factory=list)
    likely_causes: list[str] = Field(default_factory=list)
    vibration_signatures: list[str] = Field(default_factory=list)
    confirm_tests: list[str] = Field(default_factory=list)
    fixes: list[str] = Field(default_factory=list)
    notes: str = ""

    source_file: str = ""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

_TABLE_ROW_RE = re.compile(
    r"\|\s*\*\*(?P<key>[^*]+)\*\*\s*\|\s*(?P<value>.*?)\s*\|"
)

_SECTION_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)

_TAG_LINE_RE = re.compile(r"\*\*Tags:\*\*\s*(.+)")


def _extract_section(body: str, heading: str) -> str:
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\n---|\Z)"
    m = re.search(pattern, body, flags=re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_section_fuzzy(body: str, candidates: list[str]) -> str:
    for heading in candidates:
        text = _extract_section(body, heading)
        if text:
            return text
    return ""


def _parse_bullets(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def _parse_numbered(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        m = re.match(r"^\d+\.\s+(.+)", stripped)
        if m:
            items.append(m.group(1).strip())
    return items


def _parse_tags_line(body: str) -> list[str]:
    m = _TAG_LINE_RE.search(body)
    if not m:
        return []
    raw = m.group(1)
    return [t.strip().strip("`") for t in raw.split(",") if t.strip()]


# ---------------------------------------------------------------------------
# Format A: YAML front matter
# ---------------------------------------------------------------------------

def _parse_yaml_format(text: str, source_file: str) -> FaultCard:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"No YAML front matter in {source_file}")

    raw_yaml, body = match.groups()
    meta: dict[str, Any] = yaml.safe_load(raw_yaml) or {}

    refs_raw = meta.get("references") or []
    references = [
        Reference(
            title=str(r.get("title", "")),
            source=str(r.get("source", "")),
            url=str(r.get("url", "")),
        )
        for r in refs_raw
        if isinstance(r, dict)
    ]

    return FaultCard(
        id=str(meta.get("id", "")),
        fault_name=str(meta.get("fault_name", "")),
        aliases=list(meta.get("aliases") or []),
        category=str(meta.get("category", "")),
        bearing_components=list(meta.get("bearing_components") or []),
        observability_from_vibration=str(meta.get("observability_from_vibration", "")),
        diagnostic_confidence=str(meta.get("confidence", "")),
        tags=list(meta.get("tags") or []),
        references=references,
        symptoms=_parse_bullets(
            _extract_section_fuzzy(body, ["Symptoms"])
        ),
        likely_causes=_parse_bullets(
            _extract_section_fuzzy(body, ["Likely causes", "Likely Causes"])
        ),
        vibration_signatures=_parse_bullets(
            _extract_section_fuzzy(body, [
                "Expected vibration signatures",
                "Vibration / Diagnostic Signatures",
            ])
        ),
        confirm_tests=_parse_bullets(
            _extract_section_fuzzy(body, [
                "Confirm tests", "Confirmatory Tests",
            ])
        ),
        fixes=_parse_bullets(
            _extract_section_fuzzy(body, ["Fixes", "Recommended Fixes"])
        ),
        notes=_extract_section_fuzzy(body, ["Notes"]),
        source_file=source_file,
    )


# ---------------------------------------------------------------------------
# Format B: Markdown table
# ---------------------------------------------------------------------------

def _parse_table_format(text: str, source_file: str) -> FaultCard:
    title_m = re.match(r"^#\s+(.+)", text)
    fault_name = title_m.group(1).strip() if title_m else ""

    table_fields: dict[str, str] = {}
    for m in _TABLE_ROW_RE.finditer(text):
        table_fields[m.group("key").strip()] = m.group("value").strip()

    aliases_raw = table_fields.get("Aliases", "")
    aliases = [a.strip() for a in re.split(r"\s*\|\s*", aliases_raw) if a.strip()]

    components_raw = table_fields.get("Affected Components", "")
    bearing_components = [
        c.strip() for c in re.split(r"[,|]", components_raw) if c.strip()
    ]

    ref_text = _extract_section_fuzzy(text, ["References"])
    ref_bullets = _parse_numbered(ref_text) or _parse_bullets(ref_text)
    references = [Reference(title=r) for r in ref_bullets]

    tags = _parse_tags_line(text)

    return FaultCard(
        id=table_fields.get("ID", ""),
        fault_name=fault_name,
        aliases=aliases,
        category=table_fields.get("Category", ""),
        bearing_components=bearing_components,
        observability_from_vibration=table_fields.get("Observability from Vibration", ""),
        diagnostic_confidence=table_fields.get("Diagnostic Confidence", ""),
        tags=tags,
        references=references,
        symptoms=_parse_bullets(
            _extract_section_fuzzy(text, ["Symptoms"])
        ),
        likely_causes=_parse_bullets(
            _extract_section_fuzzy(text, ["Likely Causes", "Likely causes"])
        ),
        vibration_signatures=_parse_bullets(
            _extract_section_fuzzy(text, [
                "Vibration / Diagnostic Signatures",
                "Expected vibration signatures",
            ])
        ),
        confirm_tests=_parse_bullets(
            _extract_section_fuzzy(text, [
                "Confirmatory Tests", "Confirm tests",
            ])
        ),
        fixes=_parse_bullets(
            _extract_section_fuzzy(text, ["Recommended Fixes", "Fixes"])
        ),
        notes=_extract_section_fuzzy(text, ["Notes"]),
        source_file=source_file,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect_format(text: str) -> str:
    """Return 'yaml' or 'table' depending on the card's on-disk format."""
    if _FRONTMATTER_RE.match(text):
        return "yaml"
    return "table"


def parse_fault_card(path: Path) -> FaultCard:
    """Parse a single .md fault card (auto-detects format)."""
    text = path.read_text(encoding="utf-8")
    fmt = detect_format(text)
    if fmt == "yaml":
        return _parse_yaml_format(text, path.name)
    return _parse_table_format(text, path.name)


def load_fault_cards(directory: Path) -> list[FaultCard]:
    """Load every .md fault card from *directory*, sorted by ID."""
    cards: list[FaultCard] = []
    for md_path in sorted(directory.glob("*.md")):
        try:
            cards.append(parse_fault_card(md_path))
        except Exception as exc:
            print(f"[WARN] skipping {md_path.name}: {exc}")
    cards.sort(key=lambda c: c.id)
    return cards


def cards_to_json(cards: list[FaultCard]) -> list[dict[str, Any]]:
    """Serialise a list of FaultCards to plain dicts (JSON-ready)."""
    return [c.model_dump() for c in cards]


def format_card_for_llm(card: FaultCard) -> str:
    """Render a card as compact text suitable for LLM context injection."""
    lines = [
        f"### {card.fault_name}  (ID: {card.id})",
        f"Category: {card.category}",
    ]
    if card.aliases:
        lines.append(f"Aliases: {', '.join(card.aliases)}")
    if card.bearing_components:
        lines.append(f"Components: {', '.join(card.bearing_components)}")
    lines.append(f"Vibration observability: {card.observability_from_vibration}")
    lines.append(f"Diagnostic confidence: {card.diagnostic_confidence}")

    def _section(title: str, items: list[str]) -> None:
        if items:
            lines.append(f"**{title}:**")
            for item in items:
                lines.append(f"  - {item}")

    _section("Symptoms", card.symptoms)
    _section("Likely causes", card.likely_causes)
    _section("Vibration signatures", card.vibration_signatures)
    _section("Confirmatory tests", card.confirm_tests)
    _section("Fixes", card.fixes)

    if card.references:
        lines.append("**References:**")
        for ref in card.references:
            parts = [ref.title]
            if ref.source:
                parts.append(f"({ref.source})")
            if ref.url:
                parts.append(ref.url)
            lines.append(f"  - {' '.join(parts)}")

    if card.notes:
        lines.append(f"_Notes: {card.notes}_")

    return "\n".join(lines)
