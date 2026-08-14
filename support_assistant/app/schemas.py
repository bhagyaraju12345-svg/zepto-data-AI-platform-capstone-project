from pydantic import BaseModel, Field
from typing import List

class AskRequest(BaseModel):
    query: str = Field(..., description="The user's query to the support assistant.")

class AskResponse(BaseModel):
    answer: str = Field(..., description="Grounded answer to user query.")
    sources: List[str] = Field(default_factory=list, description="IDs of documents/chunks used.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0.")