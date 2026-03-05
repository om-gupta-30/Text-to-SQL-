from pydantic import BaseModel, Field
from typing import List, Dict, Any


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural language query")


class QueryResponse(BaseModel):
    question: str
    sql: str
    results: List[Dict[str, Any]]


class ErrorResponse(BaseModel):
    error: str
    details: str | None = None
