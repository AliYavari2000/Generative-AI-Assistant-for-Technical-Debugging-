import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field

from app.knowledge_base import (
    build_kb_context,
    ensure_index,
    get_all_cards,
    reload,
    search_cards,
)
from app.prompt import build_system_prompt
from app.schema import Diagnosis

load_dotenv()


def _get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")
    return OpenAI(api_key=api_key)


app = FastAPI(
    title="Technical Debugging Assistant",
    description="Paste a log snippet and get a structured JSON fault diagnosis.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class DiagnoseRequest(BaseModel):
    log_snippet: str = Field(
        min_length=1,
        description="The log snippet, sensor data, or symptom description to diagnose",
    )


class DiagnoseResponse(BaseModel):
    diagnosis: Diagnosis
    retrieved_chunks: list[str] = Field(
        default_factory=list,
        description="Chunk IDs that were provided as context for this diagnosis",
    )


# ---------------------------------------------------------------------------
# Routes — UI
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))


# ---------------------------------------------------------------------------
# Routes — Diagnosis
# ---------------------------------------------------------------------------

@app.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose(request: DiagnoseRequest):
    client = _get_openai_client()

    kb_context, chunk_ids = build_kb_context(request.log_snippet, top_k=8)
    system_prompt = build_system_prompt(kb_context)

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.log_snippet},
        ],
        response_format=Diagnosis,
        temperature=0.2,
    )

    parsed = completion.choices[0].message.parsed
    if parsed is None:
        raise HTTPException(
            status_code=502,
            detail="Model refused or failed to produce structured output",
        )

    return DiagnoseResponse(diagnosis=parsed, retrieved_chunks=chunk_ids)


# ---------------------------------------------------------------------------
# Routes — Knowledge Base
# ---------------------------------------------------------------------------

@app.get("/kb/cards")
async def list_cards(
    q: Optional[str] = Query(None, description="Keyword search across all fields"),
    category: Optional[str] = Query(None, description="Filter by category"),
    top_k: int = Query(20, ge=1, le=100),
):
    """Return fault cards, optionally filtered by keyword or category."""
    if q:
        cards = search_cards(q, category=category, top_k=top_k)
    elif category:
        cards = [c for c in get_all_cards() if c.category == category][:top_k]
    else:
        cards = get_all_cards()[:top_k]
    return [c.model_dump() for c in cards]


@app.get("/kb/cards/{card_id}")
async def get_card(card_id: str):
    """Retrieve a single fault card by ID."""
    for card in get_all_cards():
        if card.id == card_id:
            return card.model_dump()
    raise HTTPException(status_code=404, detail=f"Card {card_id} not found")


@app.post("/kb/reload")
async def reload_kb():
    """Re-read fault cards from disk (useful after adding new cards)."""
    count = reload()
    return {"status": "ok", "cards_loaded": count}


@app.post("/kb/embed")
async def build_embeddings_endpoint(force: bool = Query(False)):
    """
    Build (or rebuild) the ChromaDB vector index for all fault-card chunks.

    Chunks are embedded via OpenAI text-embedding-3-small and stored in
    a persistent ChromaDB collection so hybrid search works automatically
    on subsequent server starts.
    """
    count = ensure_index(force=force)
    return {"status": "ok", "chunks_indexed": count}
