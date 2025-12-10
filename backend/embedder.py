# # backend/embedder.py

# import os
# from typing import List, Union

# import cohere
# from cohere import Client
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Cohere API Key
# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# if not COHERE_API_KEY:
#     raise ValueError("COHERE_API_KEY environment variable not set.")

# # Note: Gemini is still used for generation in agent_config.py,
# # this file is specifically for embeddings using Cohere.


# class Embedder:
#     """
#     A class to handle text embedding using the Cohere API.
#     """

#     def __init__(self, model: str = "embed-english-v3.0"):
#         """
#         Initializes the Embedder with a specific Cohere embedding model.

#         Args:
#             model (str): The name of the embedding model to use.
#                          Defaults to "embed-english-v3.0".
#                          This model typically has a dimension of 1024.
#         """
#         self.model = model
#         self.co = Client(COHERE_API_KEY)

#     def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
#         """
#         Generates embeddings for a given text or list of texts using Cohere.

#         Args:
#             texts (Union[str, List[str]]): A single text string or a list of text strings.

#         Returns:
#             List[List[float]]: A list of embeddings. If a single string was input,
#                                it returns a list containing one embedding.
#         """
#         if isinstance(texts, str):
#             texts = [texts]

#         try:
#             response = self.co.embed(
#                 texts=texts,
#                 model=self.model,
#                 input_type="search_document"  # Use 'search_document' for documents to be indexed
#             )
#             return response.embeddings
#         except Exception as e:
#             print(f"An error occurred during Cohere embedding: {e}")
#             raise

#     def embed_query(self, query: str) -> List[float]:
#         """
#         Generates an embedding for a single query using Cohere.

#         Args:
#             query (str): The query text.

#         Returns:
#             List[float]: The embedding for the query.
#         """
#         try:
#             response = self.co.embed(
#                 texts=[query],
#                 model=self.model,
#                 input_type="search_query"  # Use 'search_query' for search queries
#             )
#             return response.embeddings[0]
#         except Exception as e:
#             print(f"An error occurred during Cohere query embedding: {e}")
#             raise


# # Singleton instance
# embedder = Embedder()


# backend/embedder.py
import os
from dotenv import load_dotenv
import cohere

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not set")

co = cohere.Client(COHERE_API_KEY)

# Cohere embedding model
MODEL = "embed-english-v3.0"


class Embedder:
    def embed(self, texts):
        """
        Used during ingestion (multiple texts).
        Returns a list of embeddings.
        """
        response = co.embed(
            model=MODEL,
            texts=texts,
            input_type="search_document"   # ✅ REQUIRED for embeddings
        )
        return response.embeddings

    def embed_query(self, text: str):
        """
        Used during query (single text).
        Returns a single embedding vector.
        """
        response = co.embed(
            model=MODEL,
            texts=[text],
            input_type="search_query"      # ✅ REQUIRED for query embeddings
        )
        return response.embeddings[0]


embedder = Embedder()
