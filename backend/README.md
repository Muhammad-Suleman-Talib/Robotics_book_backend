# RAG Chatbot Backend

This project is a complete backend for a Retrieval-Augmented Generation (RAG) chatbot system.

- **FastAPI**: For the asynchronous API.
- **Qdrant Cloud**: For efficient vector storage and retrieval.
- **Neon Postgres**: For storing metadata and chat conversation history.
- **Cohere API**: For text embedding generation.
- **OpenAI-compatible client**: For the generative reasoning agent (configured for Gemini).

## Project Structure

```
backend/
├── main.py           # FastAPI application entry point
├── ingest.py         # Script to ingest and process documents
├── query.py          # Core RAG query logic
├── neon.py           # Neon Postgres database interactions
├── qdrant_client.py  # Qdrant Cloud client and interactions
├── embedder.py       # Handles text embedding using Cohere
├── agent_config.py   # Configures the reasoning agent (uses OpenAI-compatible client for Gemini)
├── prompt.py         # System prompt for the agent
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── utils/
    └── chunker.py    # Custom word-based text chunking
```

## Setup Instructions

### 1. Clone the Repository

Clone this project to your local machine.

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install all the required packages using pip.
*Note: We use custom chunking, so `langchain` is not required for that part.*

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend` directory and add the following variables. Replace the placeholder values with your actual credentials.

```env
# backend/.env

# Neon Postgres Database URL
NEON_DATABASE_URL="postgres://user:password@host:port/dbname"

# Qdrant Cloud Credentials
QDRANT_URL="https://your-qdrant-cluster-url.qdrant.tech:6333"
QDRANT_API_KEY="your-qdrant-api-key"

# Cohere API Key for Embeddings
COHERE_API_KEY="your-cohere-api-key"

# OpenAI-compatible API Key for Generative Model (using Gemini API key if via proxy)
# This key is used for the generative model via an OpenAI-compatible client.
# If you are using a proxy to route OpenAI calls to Gemini, this should be your Gemini API Key.
OPENAI_API_KEY="your-gemini-api-key-for-openai-client"
# OpenAI-compatible API Base URL (e.g., for a Gemini proxy)
# This should point to the endpoint of your OpenAI-compatible service or proxy.
# Example: "http://localhost:8000/v1" or an actual Google API endpoint if it supports OpenAI format.
OPENAI_API_BASE="your-openai-compatible-gemini-proxy-url"
```

## Usage

### 1. Ingest Documents

First, you need to process your documents (e.g., books, articles) and store them in the Qdrant vector database.
Place your document files (e.g., `.txt`, `.pdf`, `.md`, `.mdx`, `.docx`) into a folder named `docs` within the `backend` directory (i.e., `backend/docs/`).

Run the ingestion script:

```sh
python -m backend.ingest --docs_folder backend/docs
```
*Note: For the first run, this script also creates the necessary tables in your Neon database and the collection in Qdrant. The text is chunked into approximately 450-word segments with 50-word overlaps using a custom chunker.*
*Embedding is performed via the Cohere API, and generative responses utilize an OpenAI-compatible client, configured for Gemini.*

### 2. Run the Backend Server

Start the FastAPI server using Uvicorn.

```sh
uvicorn main:app --reload
```

The server will be running at `http://127.0.0.1:8000`.

### 3. Query the Chatbot

You can now send requests to the `/api/query` endpoint to interact with the chatbot.

**Example Request:**

```sh
curl -X POST "http://127.0.0.1:8000/api/query" \
-H "Content-Type: application/json" \
-d 
'{ 
  "query": "What is the main theme of the story?",
  "session_id": "session_12345"
}'
```

**Example Response:**

```json
{
  "response": "The main theme of the story is the struggle for identity in a dystopian society.",
  "session_id": "session_12345"
}
```