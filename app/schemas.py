from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class DetectRequest(BaseModel):
    text: str
    entities: Optional[List[str]] = None
    min_score: Optional[float] = None

class EntitySpan(BaseModel):
    type: str
    value: str
    start: int
    end: int
    score: float

class DetectResponse(BaseModel):
    entities: List[EntitySpan]

class RedactPolicy(BaseModel):
    mask_mode: str = Field("template") # template | asterisk | hash
    template: str = Field("{{ENTITY_TYPE}}")
    entities_to_mask: List[str] = Field(default_factory=list)

class RedactRequest(BaseModel):
    text: str
    policy: RedactPolicy

class RedactResponse(BaseModel):
    masked_text: str