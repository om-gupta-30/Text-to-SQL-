from openai import OpenAI
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


client: Optional[OpenAI] = None


def initialize_llm():
    """Initialize OpenAI client"""
    global client
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)


def generate_sql(question: str, schema_info: str) -> str:
    """
    Generate SQL query from natural language question using LLM
    
    Args:
        question: Natural language question
        schema_info: Database schema information
    
    Returns:
        Generated SQL query string
    """
    if client is None:
        initialize_llm()
    
    system_prompt = """You are a SQL expert. Generate SQLite queries based on user requests.

Supported statement types:
- SELECT / WITH (CTEs) — reading data
- INSERT, UPDATE, DELETE — modifying rows
- REPLACE INTO — upsert (delete existing row by primary key, then insert)
- CREATE TABLE, DROP TABLE, ALTER TABLE — schema changes
- PRAGMA <name> — SQLite settings/inspection (e.g. PRAGMA table_info(orders), PRAGMA index_list(customers), PRAGMA foreign_key_list(orders))
- EXPLAIN QUERY PLAN <select> — show how SQLite executes a query (must be followed by a SELECT)

Rules:
1. Return ONLY the SQL statement — no explanations, no markdown, no code blocks.
2. Use proper SQLite syntax.
3. For INSERT/REPLACE, always use explicit column lists.
4. For CREATE TABLE, include appropriate types and constraints.
5. Generate a single statement only (no trailing semicolons).
6. For EXPLAIN, always use "EXPLAIN QUERY PLAN SELECT ..." format.

{schema}
""".format(schema=schema_info)
    
    user_prompt = f"Generate a SQL query for: {question}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        sql = response.choices[0].message.content.strip()
        
        sql = sql.replace("```sql", "").replace("```", "").strip()
        
        return sql
    
    except Exception as e:
        raise ValueError(f"LLM error: {str(e)}")
