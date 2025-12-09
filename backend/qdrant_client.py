# backend/qdrant_client.py

import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

# Load environment variables
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set.")


class QdrantDB:
    """
    A client for interacting with a Qdrant vector database.
    """

    def __init__(self, collection_name: str = "rag_chatbot_collection"):
        """
        Initializes the QdrantDB client.

        Args:
            collection_name (str): The name of the collection to use in Qdrant.
        """
        self.collection_name = collection_name
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        self.vector_size = 768  # Based on Gemini's embedding-001 model

    def ensure_collection_exists(self):
        """
        Ensures that the specified collection exists in Qdrant. If not, it creates it.
        """
        try:
            self.client.get_collection(collection_name=self.collection_name)
            print(f"Collection '{self.collection_name}' already exists.")
        except Exception:
            print(f"Collection '{self.collection_name}' not found. Creating it now.")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size, distance=models.Distance.COSINE
                ),
            )
            print("Collection created successfully.")

    def upsert_vectors(self, vectors: List[List[float]], payloads: List[Dict[str, Any]]):
        """
        Upserts (inserts or updates) vectors and their payloads into the collection.

        Args:
            vectors (List[List[float]]): A list of embedding vectors.
            payloads (List[Dict[str, Any]]): A list of metadata payloads corresponding to each vector.
        """
        if not vectors:
            print("No vectors to upsert.")
            return

        print(f"Upserting {len(vectors)} vectors into '{self.collection_name}'...")
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=None,  # Let Qdrant assign IDs
                vectors=vectors,
                payloads=payloads,
            ),
            wait=True,
        )
        print("Upsert operation completed.")

    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Searches the collection for vectors similar to the query vector.

        Args:
            query_vector (List[float]): The embedding of the search query.
            limit (int): The maximum number of results to return.

        Returns:
            List[Dict[str, Any]]: A list of search results, including payloads.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
        )
        return [hit.payload for hit in search_result if hit.payload is not None]


# Singleton instance
qdrant_db = QdrantDB()
