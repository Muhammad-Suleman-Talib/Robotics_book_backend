# backend/ingest.py

import argparse
import asyncio
import os
from pathlib import Path
from typing import Any, Dict, List

from backend.embedder import embedder
from backend.file_loader import load_document
from backend.neon import neon_db
from backend.qdrant_client import qdrant_db
from backend.utils.chunker import word_chunker


def chunk_text(
    text: str,
    file_name: str,
    chunk_size_words: int = 450,
    overlap_words: int = 50,
) -> List[Dict[str, Any]]:
    """
    Splits a long text into smaller chunks based on word count with metadata.
    """
    print(f"Chunking text for {file_name}...")
    raw_chunks = word_chunker(text, chunk_size_words, overlap_words)
    
    # Add metadata to each chunk
    chunks_with_metadata = []
    for i, chunk in enumerate(raw_chunks):
        chunks_with_metadata.append(
            {
                "chunk": chunk,
                "file_name": file_name,
                "chunk_index": i,
            }
        )
    print(f"Text split into {len(chunks_with_metadata)} chunks.")
    return chunks_with_metadata


async def main(docs_folder: str):
    """
    The main pipeline for ingestion:
    1. Initializes databases.
    2. Scans the docs_folder for supported documents.
    3. Reads, cleans, and chunks each document.
    4. Generates embeddings for chunks.
    5. Upserts the vectors and payloads to Qdrant.
    6. Stores file metadata in Neon Postgres.
    """
    # 1. Initialize databases
    print("Initializing databases...")
    await neon_db.init_db()  # Ensures chat_history and ingested_files tables exist
    qdrant_db.ensure_collection_exists()

    docs_path = Path(docs_folder)
    if not docs_path.is_dir():
        raise FileNotFoundError(f"Documentation folder not found at: {docs_folder}")

    supported_extensions = {".txt", ".pdf", ".md", ".mdx", ".docx"}
    files_to_ingest = []

    for root, _, files in os.walk(docs_path):
        for file in files:
            file_extension = Path(file).suffix.lower()
            if file_extension in supported_extensions:
                files_to_ingest.append(Path(root) / file)
    
    if not files_to_ingest:
        print(f"No supported documents found in {docs_folder}. Supported types: {', '.join(supported_extensions)}")
        return

    print(f"Found {len(files_to_ingest)} documents to ingest.")

    for file_path in files_to_ingest:
        file_name = file_path.name
        print(f"\n--- Processing {file_name} ---")

        # Load and clean document text
        document_text = load_document(str(file_path))
        if not document_text:
            print(f"Skipping {file_name} due to empty or unreadable content.")
            continue

        # Chunk the text
        chunks_with_metadata = chunk_text(document_text, file_name)
        total_chunks_count = len(chunks_with_metadata)

        if not chunks_with_metadata:
            print(f"No text chunks to process for {file_name}. Skipping.")
            continue

        # Generate embeddings
        print("Generating embeddings for text chunks...")
        embeddings = embedder.embed([c["chunk"] for c in chunks_with_metadata])

        # Prepare payloads and upsert to Qdrant
        payloads = chunks_with_metadata  # chunks_with_metadata already contains the payload structure
        qdrant_db.upsert_vectors(vectors=embeddings, payloads=payloads)

        # Store file metadata in Neon Postgres
        await neon_db.add_ingested_file_metadata(
            file_name=file_name,
            file_path=str(file_path),
            total_chunks=total_chunks_count
        )

        print(f"--- Finished processing {file_name} ---")

    print("\n--- Ingestion process completed successfully for all documents! ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents from a folder for the RAG chatbot.")
    parser.add_argument(
        "--docs_folder",
        type=str,
        default="backend/docs",
        help="The path to the folder containing document files (e.g., .pdf, .txt, .md, .docx). "
             "Defaults to 'backend/docs'.",
    )
    args = parser.parse_args()

    asyncio.run(main(args.docs_folder))
