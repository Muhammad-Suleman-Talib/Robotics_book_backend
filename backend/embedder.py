# backend/embedder.py

import os
from typing import List, Union

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=GOOGLE_API_KEY)

# Note on "OpenAI Agents SDK" for Embeddings:
# This embedder directly uses Google's `google.generativeai` library
# to generate embeddings via the Gemini API. This is the most direct and
# recommended way to interact with Gemini's embedding models.
# If the intention for "OpenAI Agents SDK" was to use an OpenAI-compatible
# API client that *routes* to Gemini, that would typically require
# a proxy or a specialized library not directly provided by Google or OpenAI.
# For direct Gemini embedding, this implementation is correct.


class Embedder:
    """
    A class to handle text embedding using the Google Gemini API.
    """

    def __init__(self, model: str = "models/embedding-001"):
        """
        Initializes the Embedder with a specific Gemini embedding model.

        Args:
            model (str): The name of the embedding model to use.
                         Defaults to "models/embedding-001".
        """
        self.model = model

    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generates embeddings for a given text or list of texts.

        Args:
            texts (Union[str, List[str]]): A single text string or a list of text strings.

        Returns:
            List[List[float]]: A list of embeddings. If a single string was input,
                               it returns a list containing one embedding.
        """
        if isinstance(texts, str):
            texts = [texts]

        try:
            result = genai.embed_content(
                model=self.model,
                content=texts,
                task_type="RETRIEVAL_DOCUMENT",  # Use "RETRIEVAL_DOCUMENT" for documents to be indexed
            )
            return result["embedding"]
        except Exception as e:
            print(f"An error occurred during embedding: {e}")
            # Depending on the use case, you might want to return an empty list
            # or re-raise the exception.
            raise

    def embed_query(self, query: str) -> List[float]:
        """
        Generates an embedding for a single query.

        Args:
            query (str): The query text.

        Returns:
            List[float]: The embedding for the query.
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="RETRIEVAL_QUERY",  # Use "RETRIEVAL_QUERY" for search queries
            )
            return result["embedding"]
        except Exception as e:
            print(f"An error occurred during query embedding: {e}")
            raise


# Singleton instance
embedder = Embedder()
