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
    
    system_prompt = """You are a SQL expert. Generate SQLite queries based on user questions.

Rules:
1. Only generate SELECT queries
2. Return ONLY the SQL query, no explanations
3. Use proper SQLite syntax
4. Do not include markdown formatting or code blocks
5. Ensure queries are safe and read-only

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
