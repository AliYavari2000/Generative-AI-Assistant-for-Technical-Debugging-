"""
Chunker for fault cards.

Breaks each FaultCard into section-level chunks with unique IDs
(e.g. ``BRG-002::symptoms``) so the RAG pipeline can retrieve and
cite fine-grained passages rather than whole cards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.fault_card_parser import FaultCard


@dataclass
class Chunk:
    chunk_id: str
    card_id: str
    card_name: str
    section: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


def _bullet_block(title: str, items: list[str]) -> str:
    return f"{title}:\n" + "\n".join(f"- {item}" for item in items)


def chunk_card(card: FaultCard) -> list[Chunk]:
    """Split a single FaultCard into one chunk per non-empty section."""
    base_meta = {"category": card.category, "tags": ",".join(card.tags)}
    chunks: list[Chunk] = []

    def _add(section: str, content: str) -> None:
        header = f"{card.fault_name} ({card.id})"
        chunks.append(Chunk(
            chunk_id=f"{card.id}::{section}",
            card_id=card.id,
            card_name=card.fault_name,
            section=section,
            content=f"{header} — {content}",
            metadata=dict(base_meta),
        ))

    overview_parts = [
        f"Fault: {card.fault_name}",
        f"ID: {card.id}",
        f"Category: {card.category}",
    ]
    if card.aliases:
        overview_parts.append(f"Aliases: {', '.join(card.aliases)}")
    if card.bearing_components:
        overview_parts.append(f"Components: {', '.join(card.bearing_components)}")
    if card.observability_from_vibration:
        overview_parts.append(
            f"Vibration observability: {card.observability_from_vibration}"
        )
    if card.diagnostic_confidence:
        overview_parts.append(
            f"Diagnostic confidence: {card.diagnostic_confidence}"
        )
    _add("overview", "\n".join(overview_parts))

    section_defs: list[tuple[str, str, list[str]]] = [
        ("symptoms", "Symptoms", card.symptoms),
        ("likely_causes", "Likely causes", card.likely_causes),
        ("vibration_signatures", "Vibration signatures", card.vibration_signatures),
        ("confirm_tests", "Confirmatory tests", card.confirm_tests),
        ("fixes", "Fixes", card.fixes),
    ]
    for key, title, items in section_defs:
        if items:
            _add(key, _bullet_block(title, items))

    if card.notes:
        _add("notes", f"Notes:\n{card.notes}")

    return chunks


def chunk_all_cards(cards: list[FaultCard]) -> list[Chunk]:
    """Chunk every card and return a flat list."""
    chunks: list[Chunk] = []
    for card in cards:
        chunks.extend(chunk_card(card))
    return chunks
