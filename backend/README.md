# RAG Chatbot Backend

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![Cohere](https://img.shields.io/badge/Cohere-Embed-blue)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-red)
![Neon](https://img.shields.io/badge/Neon-Postgres-lightgrey)

This repository contains the complete backend for a sophisticated Retrieval-Augmented Generation (RAG) chatbot. It's designed to answer questions based on a given set of documents, using a powerful combination of vector search and large language models.

## 🚀 Features

*   **Retrieval-Augmented Generation (RAG):** Provides context-aware answers by retrieving relevant information from your documents before generating a response.
*   **Multi-format Document Ingestion:** Supports a wide range of document formats including `.txt`, `.pdf`, `.md`, `.mdx`, and `.docx`.
*   **Custom Text Chunking:** Implements a custom word-based chunking strategy to optimize the context provided to the language model.
*   **Vector Database Integration:** Uses Qdrant Cloud for efficient storage and retrieval of text embeddings.
*   **Persistent Chat History:** Stores conversation history in a Neon Postgres database, allowing for multi-turn conversations.
*   **Pluggable AI Models:** Easily switch between different embedding and generation models. Currently configured to use Cohere for embeddings and an OpenAI-compatible client for generation (e.g., Gemini).
*   **Asynchronous API:** Built with FastAPI for high performance and scalability.

## 🛠️ Technologies Used

*   **Framework:** FastAPI
*   **Vector Database:** Qdrant Cloud
*   **Database:** Neon Postgres
*   **Embedding Model:** Cohere
*   **Generative Model:** OpenAI-compatible client (e.g., Gemini)
*   **Libraries:**
    *   `uvicorn` for serving the application.
    *   `pydantic` for data validation.
    *   `qdrant-client` for interacting with Qdrant.
    *   `asyncpg` for asynchronous Postgres interaction.
    *   `cohere` for generating text embeddings.
    *   `openai` for the generative model client.
    *   `pypdf`, `python-docx` for parsing different document formats.
    *   `python-dotenv` for managing environment variables.
    *   `tiktoken` for token counting.

## Project Structure

```
backend/
├── main.py           # FastAPI application entry point
├── ingest.py         # Script to ingest and process documents
├── query.py          # Core RAG query logic
├── neon.py           # Neon Postgres database interactions
├── qdrant_client.py  # Qdrant Cloud client and interactions
├── embedder.py       # Handles text embedding using Cohere
├── agent_config.py   # Configures the reasoning agent
├── prompt.py         # System prompt for the agent
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── utils/
    └── chunker.py    # Custom word-based text chunking
```

## ⚙️ Setup and Installation

### 1. Clone the Repository

```sh
git clone https://github.com/Muhammad-Suleman-Talib/Robotics_book_backend.git
cd Robotics_book_backend
```

### 2. Create a Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### 3. Install Dependencies

```sh
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend` directory and add your credentials.

```env
# backend/.env

# Neon Postgres Database URL
NEON_DATABASE_URL="postgres://user:password@host:port/dbname"

# Qdrant Cloud Credentials
QDRANT_URL="https://your-qdrant-cluster-url.qdrant.tech:6333"
QDRANT_API_KEY="your-qdrant-api-key"

# Cohere API Key for Embeddings
COHERE_API_KEY="your-cohere-api-key"

# OpenAI-compatible API Key for Generative Model
OPENAI_API_KEY="your-gemini-api-key-for-openai-client"
# OpenAI-compatible API Base URL
OPENAI_API_BASE="your-openai-compatible-gemini-proxy-url"
```

## 🚀 Usage

### 1. Ingest Documents

Place your documents in the `backend/docs` folder and run the ingestion script:

```sh
python -m backend.ingest --docs_folder backend/docs
```

This will process the documents, create embeddings, and store them in your Qdrant collection. It will also set up the necessary tables in your Neon database.

### 2. Run the Backend Server

```sh
uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 📡 API Endpoints

The API is documented with Swagger UI, available at `http://127.0.0.1:8000/docs`.

### `POST /api/query`

Handles a user query by processing it through the RAG pipeline.

**Request Body:**

```json
{
  "query": "What is the main theme of the story?",
  "session_id": "session_12345",
  "selected_text": "Optional selected text from the document to focus the query."
}
```

**Response:**

```json
{
  "response": "The main theme of the story is...",
  "session_id": "session_12345"
}
```

### `GET /`

A simple root endpoint to confirm the server is running.

### `GET /health`

A health check endpoint that returns the server status.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a pull request.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
