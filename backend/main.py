# # backend/main.py

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional

# from backend.query import process_query
# from backend.neon import neon_db

# # Initialize FastAPI app
# app = FastAPI(
#     title="RAG Chatbot API",
#     description="An API for a Retrieval-Augmented Generation chatbot.",
#     version="1.0.0",
# )


# # --- Pydantic Models ---
# class QueryRequest(BaseModel):
#     query: str
#     session_id: str
#     selected_text: Optional[str] = None


# class QueryResponse(BaseModel):
#     response: str
#     session_id: str

# @app.get("/")
# def read_root():
#     """A simple root endpoint to confirm the server is running."""
#     return {"message": "Welcome to the RAG Chatbot API. Use the /api/query endpoint to interact."}

# # --- API Endpoints ---
# # @app.post("/api/query", response_model=QueryResponse)
# # async def handle_query(request: QueryRequest):
# #     """
# #     Handles a user query by processing it through the RAG pipeline
# #     and storing the conversation turn in the database.
# #     """
# #     if not request.query:
# #         raise HTTPException(status_code=400, detail="Query cannot be empty.")
# #     if not request.session_id:
# #         raise HTTPException(status_code=400, detail="Session ID must be provided.")

# #     try:
# #         # Process the query to get the agent's response
# #         result = await process_query(
# #             query=request.query,
# #             session_id=request.session_id,
# #             selected_text=request.selected_text
# #         )

# #         # Store the user's message and the assistant's response in the database
# #         await neon_db.add_chat_message(
# #             session_id=request.session_id, role="user", message=request.query
# #         )
# #         await neon_db.add_chat_message(
# #             session_id=result["session_id"], role="assistant", message=result["response"]
# #         )

# #         return QueryResponse(
# #             response=result["response"],
# #             session_id=result["session_id"]
# #         )

# #     except Exception as e:
# #         print(f"An error occurred during query processing: {e}")
# #         raise HTTPException(status_code=500, detail="An internal server error occurred.")

# @app.post("/api/query", response_model=QueryResponse)
# async def handle_query(request: QueryRequest):
#     """
#     Handles a user query safely through the RAG pipeline.
#     Returns clean JSON even when context is missing or an exception occurs.
#     """

#     # ✅ Validate input
#     if not request.query:
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")
#     if not request.session_id:
#         raise HTTPException(status_code=400, detail="Session ID must be provided.")

#     try:
#         # ✅ Run RAG pipeline
#         result = await process_query(
#             query=request.query,
#             session_id=request.session_id,
#             selected_text=request.selected_text
#         )

#         response_text = result.get("response", "")
#         session_id = result.get("session_id", request.session_id)

#         # ✅ Safety fallback if RAG returns empty answer
#         if not response_text:
#             response_text = "Sorry, I could not find relevant information in the documents."

#         # ✅ Store conversation in DB (async safe)
#         await neon_db.add_chat_message(
#             session_id=session_id, role="user", message=request.query
#         )
#         await neon_db.add_chat_message(
#             session_id=session_id, role="assistant", message=response_text
#         )

#         return QueryResponse(
#             response=response_text,
#             session_id=session_id
#         )

#     except Exception as e:
#         # ✅ Log error for debugging
#         print(f"[ERROR] Query failed: {e}")

#         # ✅ Return safe JSON response instead of crashing server
#         return QueryResponse(
#             response="Internal server error. Please try again later.",
#             session_id=request.session_id
#         )



# # --- Health Check Endpoint ---
# @app.get("/health")
# def health_check():
#     """Provides a simple health check endpoint."""
#     return {"status": "ok"}



# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from backend.query import process_query
from backend.neon import neon_db

# ----------------------------------------------------------
# Initialize FastAPI app
# ----------------------------------------------------------
app = FastAPI(
    title="RAG Chatbot API",
    description="An API for a Retrieval-Augmented Generation chatbot.",
    version="1.0.0",
)

# ✅ FIX: Enable CORS (removes 405 errors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------
# Pydantic Models
# ----------------------------------------------------------
class QueryRequest(BaseModel):
    query: str
    session_id: str
    selected_text: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
def read_root():
    return {"message": "API running"}

# ----------------------------------------------------------
# API Endpoint
# ----------------------------------------------------------
@app.post("/api/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):

    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if not request.session_id:
        raise HTTPException(status_code=400, detail="Session ID must be provided.")

    try:
        result = await process_query(
            query=request.query,
            session_id=request.session_id,
            selected_text=request.selected_text,
        )

        response_text = result.get("response", "")
        session_id = result.get("session_id", request.session_id)

        if not response_text:
            response_text = "Sorry, I could not find relevant information in the documents."

        await neon_db.add_chat_message(session_id=session_id, role="user", message=request.query)
        await neon_db.add_chat_message(session_id=session_id, role="assistant", message=response_text)

        return QueryResponse(response=response_text, session_id=session_id)

    except Exception as e:
        print(f"[ERROR] Query failed: {e}")

        return QueryResponse(
            response="Internal server error. Please try again later.",
            session_id=request.session_id,
        )




@app.get("/health")
def health_check():
    return {"status": "ok"}
