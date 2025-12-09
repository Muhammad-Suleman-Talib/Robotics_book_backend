# backend/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.query import process_query
from backend.neon import neon_db

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="An API for a Retrieval-Augmented Generation chatbot.",
    version="1.0.0",
)


# --- Pydantic Models ---
class QueryRequest(BaseModel):
    query: str
    session_id: str
    selected_text: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    session_id: str


# --- API Endpoints ---
@app.post("/api/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Handles a user query by processing it through the RAG pipeline
    and storing the conversation turn in the database.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    if not request.session_id:
        raise HTTPException(status_code=400, detail="Session ID must be provided.")

    try:
        # Process the query to get the agent's response
        result = await process_query(
            query=request.query,
            session_id=request.session_id,
            selected_text=request.selected_text
        )

        # Store the user's message and the assistant's response in the database
        await neon_db.add_chat_message(
            session_id=request.session_id, role="user", message=request.query
        )
        await neon_db.add_chat_message(
            session_id=result["session_id"], role="assistant", message=result["response"]
        )

        return QueryResponse(
            response=result["response"],
            session_id=result["session_id"]
        )

    except Exception as e:
        print(f"An error occurred during query processing: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.get("/")
def read_root():
    """A simple root endpoint to confirm the server is running."""
    return {"message": "Welcome to the RAG Chatbot API. Use the /api/query endpoint to interact."}

# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    """Provides a simple health check endpoint."""
    return {"status": "ok"}
