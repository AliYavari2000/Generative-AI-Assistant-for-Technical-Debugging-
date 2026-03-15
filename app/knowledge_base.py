"""
Fault-card knowledge base — RAG edition.

Loads every card once, chunks them, indexes into ChromaDB, and exposes
a hybrid-search API (vector + keyword via Reciprocal Rank Fusion) that
the ``/diagnose`` endpoint uses to inject relevant passages + chunk IDs
into the LLM context window.

Search strategy
---------------
1. **Hybrid search** (default) — combines vector similarity (ChromaDB +
   OpenAI embeddings) with keyword overlap, merged via RRF.
2. **Keyword fallback** — token-overlap scoring.  Used automatically when
   the vector index is empty or unavailable.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from app.chunker import Chunk, chunk_all_cards
from app.fault_card_parser import FaultCard, load_fault_cards

log = logging.getLogger(__name__)

FAULT_CARDS_DIR = Path(__file__).resolve().parent.parent / "fault_cards"

_cards: list[FaultCard] = []
_cards_by_id: dict[str, FaultCard] = {}
_chunks: list[Chunk] = []
_index_ready: bool = False


# ------------------------------------------------------------------
# Loading
# ------------------------------------------------------------------

def _ensure_loaded() -> list[FaultCard]:
    global _cards, _cards_by_id, _chunks
    if not _cards:
        _cards = load_fault_cards(FAULT_CARDS_DIR)
        _cards_by_id = {c.id: c for c in _cards}
        _chunks = chunk_all_cards(_cards)
    return _cards


def get_all_cards() -> list[FaultCard]:
    return list(_ensure_loaded())


def get_all_chunks() -> list[Chunk]:
    _ensure_loaded()
    return list(_chunks)


def reload() -> int:
    """Force-reload cards from disk.  Returns the new count."""
    global _cards, _cards_by_id, _chunks, _index_ready
    _cards = load_fault_cards(FAULT_CARDS_DIR)
    _cards_by_id = {c.id: c for c in _cards}
    _chunks = chunk_all_cards(_cards)
    _index_ready = False
    return len(_cards)


# ------------------------------------------------------------------
# Indexing
# ------------------------------------------------------------------

def ensure_index(*, force: bool = False) -> int:
    """Build (or rebuild) the ChromaDB vector index for all chunks.
    Returns the number of chunks indexed."""
    global _index_ready

    from app.vector_store import index_chunks

    _ensure_loaded()
    count = index_chunks(_chunks, force=force)
    _index_ready = True
    log.info("Vector index ready — %d chunks", count)
    return count


def _check_index() -> None:
    """Silently verify that ChromaDB has data.  If not, set the flag."""
    global _index_ready
    if _index_ready:
        return
    try:
        from app.vector_store import get_collection
        collection = get_collection()
        if collection.count() > 0:
            _index_ready = True
            log.info("ChromaDB collection found with %d chunks", collection.count())
    except Exception:
        pass


# ------------------------------------------------------------------
# Search — hybrid (vector + keyword via RRF)
# ------------------------------------------------------------------

def _hybrid_search(
    query: str,
    *,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    from app.vector_store import hybrid_search
    return hybrid_search(query, _chunks, top_k=top_k)


# ------------------------------------------------------------------
# Search — keyword fallback
# ------------------------------------------------------------------

def _keyword_search(
    query: str,
    *,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    from app.vector_store import keyword_search
    return keyword_search(query, _chunks, top_k=top_k)


# ------------------------------------------------------------------
# Public search API (card-level, backward compatible)
# ------------------------------------------------------------------

def search_cards(
    query: str,
    *,
    category: str | None = None,
    top_k: int = 5,
) -> list[FaultCard]:
    """Search fault cards by relevance.  Returns unique cards extracted
    from the top chunk hits."""
    _ensure_loaded()
    _check_index()

    if _index_ready:
        try:
            hits = _hybrid_search(query, top_k=top_k * 3)
        except Exception as exc:
            log.warning("Hybrid search failed, falling back to keyword: %s", exc)
            hits = _keyword_search(query, top_k=top_k * 3)
    else:
        hits = _keyword_search(query, top_k=top_k * 3)

    seen: set[str] = set()
    cards: list[FaultCard] = []
    for hit in hits:
        card_id = hit["metadata"]["card_id"]
        if card_id in seen:
            continue
        if category and hit["metadata"].get("category") != category:
            continue
        card = _cards_by_id.get(card_id)
        if card:
            seen.add(card_id)
            cards.append(card)
        if len(cards) >= top_k:
            break
    return cards


# ------------------------------------------------------------------
# Public search API (chunk-level, for RAG)
# ------------------------------------------------------------------

def search_chunks(
    query: str,
    *,
    top_k: int = 8,
) -> list[dict[str, Any]]:
    """Return the top-k most relevant *chunks* (not whole cards).

    Each element is a dict with keys: chunk_id, content, metadata.
    """
    _ensure_loaded()
    _check_index()

    if _index_ready:
        try:
            return _hybrid_search(query, top_k=top_k)
        except Exception as exc:
            log.warning("Hybrid search failed, falling back to keyword: %s", exc)

    return _keyword_search(query, top_k=top_k)


# ------------------------------------------------------------------
# Context builder (injects retrieved chunks into the prompt)
# ------------------------------------------------------------------

def build_kb_context(
    query: str,
    top_k: int = 8,
) -> tuple[str, list[str]]:
    """Return (formatted_context_string, list_of_chunk_ids).

    The context string is ready for injection into the system prompt.
    The chunk IDs list is returned so the API response can record which
    chunks were provided.
    """
    hits = search_chunks(query, top_k=top_k)
    if not hits:
        return "", []

    chunk_ids: list[str] = []
    passages: list[str] = []
    for hit in hits:
        cid = hit["chunk_id"]
        chunk_ids.append(cid)
        passages.append(f"[{cid}]\n{hit['content']}")

    header = (
        f"=== RETRIEVED CONTEXT ({len(hits)} chunks) ===\n"
        "Use ONLY these passages to support your claims.  "
        "Cite the bracketed chunk ID when a passage supports a hypothesis.\n\n"
    )
    return header + "\n\n---\n\n".join(passages), chunk_ids
