"""
ChromaDB-backed vector store with **hybrid search**.

Retrieval strategy
------------------
1. **Vector search** — cosine similarity via ChromaDB + OpenAI embeddings.
2. **Keyword search** — lightweight token-overlap scoring on the raw chunks.
3. **Reciprocal Rank Fusion (RRF)** — merges both ranked lists into a single
   result set, which significantly improves recall on technical text.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from app.chunker import Chunk

log = logging.getLogger(__name__)

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "fault_chunks"
EMBEDDING_MODEL = "text-embedding-3-small"


# ------------------------------------------------------------------
# ChromaDB helpers
# ------------------------------------------------------------------

def _get_embedding_fn() -> OpenAIEmbeddingFunction:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set — cannot generate embeddings")
    return OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=EMBEDDING_MODEL,
    )


def _get_client() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection() -> chromadb.Collection:
    client = _get_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_get_embedding_fn(),
        metadata={"hnsw:space": "cosine"},
    )


# ------------------------------------------------------------------
# Indexing
# ------------------------------------------------------------------

def index_chunks(chunks: list[Chunk], *, force: bool = False) -> int:
    """Upsert all chunks into ChromaDB.  With *force* the collection is
    dropped and rebuilt from scratch."""
    client = _get_client()

    if force:
        try:
            client.delete_collection(COLLECTION_NAME)
        except ValueError:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_get_embedding_fn(),
        metadata={"hnsw:space": "cosine"},
    )

    BATCH = 100
    for start in range(0, len(chunks), BATCH):
        batch = chunks[start : start + BATCH]
        collection.upsert(
            ids=[c.chunk_id for c in batch],
            documents=[c.content for c in batch],
            metadatas=[
                {
                    "card_id": c.card_id,
                    "card_name": c.card_name,
                    "section": c.section,
                    "category": c.metadata.get("category", ""),
                }
                for c in batch
            ],
        )

    log.info("Indexed %d chunks into ChromaDB", len(chunks))
    return len(chunks)


# ------------------------------------------------------------------
# Vector search
# ------------------------------------------------------------------

def vector_search(query: str, *, top_k: int = 10) -> list[dict[str, Any]]:
    """Return the *top_k* most similar chunks by embedding distance."""
    collection = get_collection()
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    hits: list[dict[str, Any]] = []
    for i in range(len(results["ids"][0])):
        hits.append({
            "chunk_id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return hits


# ------------------------------------------------------------------
# Keyword search (token-overlap scoring)
# ------------------------------------------------------------------

def keyword_search(
    query: str,
    chunks: list[Chunk],
    *,
    top_k: int = 10,
) -> list[dict[str, Any]]:
    tokens = {t.lower() for t in query.split() if len(t) > 2}
    if not tokens:
        return []

    scored: list[tuple[Chunk, int]] = []
    for chunk in chunks:
        blob = chunk.content.lower()
        score = sum(1 for t in tokens if t in blob)
        if score > 0:
            scored.append((chunk, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    return [
        {
            "chunk_id": c.chunk_id,
            "content": c.content,
            "metadata": {
                "card_id": c.card_id,
                "card_name": c.card_name,
                "section": c.section,
                "category": c.metadata.get("category", ""),
            },
        }
        for c, _ in scored[:top_k]
    ]


# ------------------------------------------------------------------
# Hybrid search (RRF)
# ------------------------------------------------------------------

def hybrid_search(
    query: str,
    chunks: list[Chunk],
    *,
    top_k: int = 5,
    vector_weight: float = 0.7,
    keyword_weight: float = 0.3,
    rrf_k: int = 60,
) -> list[dict[str, Any]]:
    """Combine vector and keyword search via Reciprocal Rank Fusion.

    ``rrf_k`` is the RRF constant (typically 60).  Higher values dampen
    the effect of rank differences.
    """
    pool_size = top_k * 3
    vec_results = vector_search(query, top_k=pool_size)
    kw_results = keyword_search(query, chunks, top_k=pool_size)

    rrf_scores: dict[str, float] = {}
    chunk_data: dict[str, dict[str, Any]] = {}

    for rank, hit in enumerate(vec_results):
        cid = hit["chunk_id"]
        rrf_scores[cid] = rrf_scores.get(cid, 0) + vector_weight / (rrf_k + rank + 1)
        chunk_data[cid] = hit

    for rank, hit in enumerate(kw_results):
        cid = hit["chunk_id"]
        rrf_scores[cid] = rrf_scores.get(cid, 0) + keyword_weight / (rrf_k + rank + 1)
        if cid not in chunk_data:
            chunk_data[cid] = hit

    ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    results: list[dict[str, Any]] = []
    for cid, score in ranked[:top_k]:
        hit = dict(chunk_data[cid])
        hit["rrf_score"] = score
        results.append(hit)

    return results
