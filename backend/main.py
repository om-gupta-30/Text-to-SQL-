from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models import QueryRequest, QueryResponse, ErrorResponse
from database import initialize_database, execute_query, get_schema_info
from llm import initialize_llm, generate_sql


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and LLM on startup"""
    initialize_database()
    initialize_llm()
    yield


app = FastAPI(
    title="Text-to-SQL API",
    description="Convert natural language queries to SQL and execute them",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Text-to-SQL API is running"}


@app.post("/query", response_model=QueryResponse, responses={400: {"model": ErrorResponse}})
async def query_database(request: QueryRequest):
    """
    Convert natural language question to SQL and execute it
    
    Flow:
    1. Receive question
    2. Call generate_sql(question)
    3. Execute SQL (only SELECT queries allowed)
    4. Return results
    
    Args:
        request: QueryRequest containing natural language question
    
    Returns:
        QueryResponse with question, SQL, and results
    
    Raises:
        HTTPException: If SQL generation or execution fails
    """
    try:
        schema_info = get_schema_info()
        
        sql = generate_sql(request.question, schema_info)
        
        results = execute_query(sql)
        
        return QueryResponse(
            question=request.question,
            sql=sql,
            results=results
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Query processing failed", "details": str(e)}
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "details": str(e)}
        )


@app.get("/schema")
async def get_schema():
    """Get database schema information"""
    return {"schema": get_schema_info()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
