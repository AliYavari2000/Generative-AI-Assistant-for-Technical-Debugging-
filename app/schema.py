from pydantic import BaseModel, Field


class Citation(BaseModel):
    chunk_id: str = Field(
        description="ID of the retrieved chunk, e.g. BRG-002::symptoms"
    )
    card_name: str = Field(
        description="Human-readable name of the fault card this chunk belongs to"
    )


class FaultHypothesis(BaseModel):
    rank: int = Field(description="Rank of this hypothesis (1 = most likely)")
    fault: str = Field(description="Short name of the suspected fault")
    reasoning: str = Field(description="Why this fault is suspected given the evidence")
    citations: list[Citation] = Field(
        default_factory=list,
        description="Chunks from the knowledge base that support this hypothesis",
    )


class Diagnosis(BaseModel):
    symptoms_detected: list[str] = Field(
        description="Observable symptoms extracted from the log or description"
    )
    top_fault_hypotheses: list[FaultHypothesis] = Field(
        description="Ranked list of most likely faults (most likely first)"
    )
    evidence_needed: list[str] = Field(
        description="Additional data or measurements that would confirm or rule out hypotheses"
    )
    next_tests: list[str] = Field(
        description="Concrete, actionable diagnostic steps the operator should take next"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall confidence in the top hypothesis (0.0 to 1.0)",
    )
