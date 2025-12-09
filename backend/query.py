# backend/query.py

from typing import Optional, Dict, Any

from backend.embedder import embedder
from backend.qdrant_client import qdrant_db
from backend.agent_config import rag_agent


async def process_query(query: str, session_id: str, selected_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Processes a user query by performing Retrieval-Augmented Generation.

    This function orchestrates the entire RAG flow:
    1.  Handles direct context if `selected_text` is provided.
    2.  If not, it embeds the user's query.
    3.  Searches the vector database (Qdrant) for relevant document chunks.
    4.  Passes the query and retrieved context to the reasoning agent (Gemini).
    5.  Returns the agent's response.

    Args:
        query (str): The user's question.
        session_id (str): A unique identifier for the conversation session.
        selected_text (Optional[str]): Text manually selected by the user to be used
                                       as the primary context.

    Returns:
        Dict[str, Any]: A dictionary containing the agent's response and the session ID.
    """
    context = []
    if selected_text:
        # If the user has highlighted or selected specific text, use it as the sole context.
        print("Using selected text as context.")
        context = [{"chunk": selected_text}]
    else:
        # Standard RAG flow: embed the query and search for context.
        print("Performing RAG search for context...")
        query_embedding = embedder.embed_query(query)
        context = qdrant_db.search(query_vector=query_embedding, limit=5)
        if not context:
            print("No relevant context found in the vector database.")

    # Get the final response from the agent
    response_text = rag_agent.get_response(query=query, context=context)

    return {
        "response": response_text,
        "session_id": session_id,
    }
