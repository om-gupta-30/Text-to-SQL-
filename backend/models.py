from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal, Optional


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural language query")


class QueryResponse(BaseModel):
    question: str
    sql: str
    query_type: Literal["select", "dml", "ddl", "pragma", "other"]
    results: List[Dict[str, Any]]
    rows_affected: Optional[int]
    message: str


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
