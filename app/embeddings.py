"""
Embedding helpers for semantic search over fault cards.

Uses OpenAI text-embedding-3-small and caches results to disk so
embeddings are only re-computed when cards change.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
CACHE_FILENAME = ".embeddings_cache.json"


# ---------------------------------------------------------------------------
# Pure-Python vector math (avoids numpy dependency)
# ---------------------------------------------------------------------------

def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    na, nb = _norm(a), _norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return _dot(a, b) / (na * nb)


# ---------------------------------------------------------------------------
# Card → text blob for embedding
# ---------------------------------------------------------------------------

def card_to_text(card: Any) -> str:
    """Flatten a FaultCard into a single string for embedding."""
    parts = [
        card.fault_name,
        ", ".join(card.aliases),
        card.category,
        ", ".join(card.bearing_components),
        "Symptoms: " + "; ".join(card.symptoms),
        "Causes: " + "; ".join(card.likely_causes),
        "Vibration signatures: " + "; ".join(card.vibration_signatures),
        "Confirmatory tests: " + "; ".join(card.confirm_tests),
        "Fixes: " + "; ".join(card.fixes),
        card.notes,
    ]
    return "\n".join(p for p in parts if p)


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Embedding via OpenAI API
# ---------------------------------------------------------------------------

def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set — cannot generate embeddings")
    return OpenAI(api_key=api_key)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts via the OpenAI API."""
    client = _get_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    response.data.sort(key=lambda d: d.index)
    return [d.embedding for d in response.data]


def embed_single(text: str) -> list[float]:
    return embed_texts([text])[0]


# ---------------------------------------------------------------------------
# Disk cache
# ---------------------------------------------------------------------------

def _cache_path(cards_dir: Path) -> Path:
    return cards_dir / CACHE_FILENAME


def load_cache(cards_dir: Path) -> dict[str, Any]:
    path = _cache_path(cards_dir)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_cache(cards_dir: Path, cache: dict[str, Any]) -> None:
    path = _cache_path(cards_dir)
    path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def build_embeddings(
    cards: list[Any],
    cards_dir: Path,
    *,
    force: bool = False,
) -> dict[str, list[float]]:
    """
    Return {card_id: embedding_vector} for every card.

    Reads from cache when a card's content hasn't changed.
    Only calls the API for new or modified cards.
    """
    cache = {} if force else load_cache(cards_dir)
    cached_vectors: dict[str, dict[str, Any]] = cache.get("vectors", {})

    to_embed: list[tuple[str, str]] = []  # (card_id, text)

    for card in cards:
        text = card_to_text(card)
        h = _content_hash(text)
        entry = cached_vectors.get(card.id)
        if entry and entry.get("hash") == h:
            continue
        to_embed.append((card.id, text))

    if to_embed:
        ids, texts = zip(*to_embed)
        vectors = embed_texts(list(texts))
        for cid, vec, txt in zip(ids, vectors, texts):
            cached_vectors[cid] = {
                "hash": _content_hash(txt),
                "vector": vec,
            }
        cache["vectors"] = cached_vectors
        cache["model"] = EMBEDDING_MODEL
        save_cache(cards_dir, cache)

    return {cid: entry["vector"] for cid, entry in cached_vectors.items()}


# ---------------------------------------------------------------------------
# Semantic search
# ---------------------------------------------------------------------------

def semantic_search(
    query: str,
    card_vectors: dict[str, list[float]],
    cards_by_id: dict[str, Any],
    *,
    top_k: int = 5,
) -> list[tuple[Any, float]]:
    """
    Embed the query and return the top-k most similar cards
    as (FaultCard, similarity_score) tuples.
    """
    q_vec = embed_single(query)

    scored = [
        (cards_by_id[cid], cosine_similarity(q_vec, vec))
        for cid, vec in card_vectors.items()
        if cid in cards_by_id
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]
