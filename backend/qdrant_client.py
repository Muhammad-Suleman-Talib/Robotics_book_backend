# # backend/qdrant_client.py

# import os
# import uuid # Import uuid
# from typing import List, Dict, Any

# from dotenv import load_dotenv
# from qdrant_client import QdrantClient, models

# # Load environment variables
# load_dotenv()

# QDRANT_URL = os.getenv("QDRANT_URL")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# if not QDRANT_URL or not QDRANT_API_KEY:
#     raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set.")


# class QdrantDB:
#     """
#     A client for interacting with a Qdrant vector database.
#     """

#     def __init__(self, collection_name: str = "docs"):
#         """
#         Initializes the QdrantDB client.

#         Args:
#             collection_name (str): The name of the collection to use in Qdrant.
#         """
#         self.collection_name = collection_name
#         self.client = QdrantClient(
#             url=QDRANT_URL,
#             api_key=QDRANT_API_KEY,
#         )
#         self.vector_size = 1024  # Based on Cohere's embed-english-v3.0 model

#     def ensure_collection_exists(self):
#         """
#         Ensures that the specified collection exists in Qdrant with the correct vector size.
#         If not, or if the vector size is mismatched, it recreates the collection.
#         """
#         collection_config_matches = False
#         try:
#             collection_info = self.client.get_collection(collection_name=self.collection_name)
#             if (
#                 collection_info.config
#                 and collection_info.config.vectors
#                 and collection_info.config.vectors.size == self.vector_size
#                 and collection_info.config.vectors.distance == models.Distance.COSINE
#             ):
#                 print(f"Collection '{self.collection_name}' already exists with correct configuration.")
#                 collection_config_matches = True
#             else:
#                 print(f"Collection '{self.collection_name}' exists but configuration is mismatched. Recreating it.")
#         except Exception:
#             print(f"Collection '{self.collection_name}' not found. Creating it now.")
        
#         if not collection_config_matches:
#             self.client.recreate_collection(
#                 collection_name=self.collection_name,
#                 vectors_config=models.VectorParams(
#                     size=self.vector_size, distance=models.Distance.COSINE
#                 ),
#             )
#             print("Collection created/recreated successfully with correct configuration.")

#     def upsert_vectors(self, vectors: List[List[float]], payloads: List[Dict[str, Any]]):
#         """
#         Upserts (inserts or updates) vectors and their payloads into the collection.

#         Args:
#             vectors (List[List[float]]): A list of embedding vectors.
#             payloads (List[Dict[str, Any]]): A list of metadata payloads corresponding to each vector.
#         """
#         if not vectors:
#             print("No vectors to upsert.")
#             return

#         # Generate UUIDs for each vector to satisfy Pydantic validation
#         ids = [str(uuid.uuid4()) for _ in vectors]

#         print(f"Upserting {len(vectors)} vectors into '{self.collection_name}'...")
#         self.client.upsert(
#             collection_name=self.collection_name,
#             points=models.Batch(
#                 ids=ids,
#                 vectors=vectors,
#                 payloads=payloads,
#             ),
#             wait=True,
#         )
#         print("Upsert operation completed.")

#     def search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
#         """
#         Searches the collection for vectors similar to the query vector.

#         Args:
#             query_vector (List[float]): The embedding of the search query.
#             limit (int): The maximum number of results to return.

#         Returns:
#             List[Dict[str, Any]]: A list of search results, including payloads.
#         """
#         search_result = self.client.search(
#             collection_name=self.collection_name,
#             query_vector=query_vector,
#             limit=limit,
#             with_payload=True,
#         )
#         return [hit.payload for hit in search_result if hit.payload is not None]


# # Singleton instance
# import os
# import uuid
# from typing import List, Dict, Any
# from dotenv import load_dotenv
# from qdrant_client import QdrantClient, models

# load_dotenv()

# QDRANT_URL = os.getenv("QDRANT_URL")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# if not QDRANT_URL or not QDRANT_API_KEY:
#     raise ValueError("Missing QDRANT_URL or QDRANT_API_KEY")


# class QdrantDB:
#     def __init__(self, collection_name: str = "docs"):
#         self.collection_name = collection_name

#         self.client = QdrantClient(
#             url=QDRANT_URL,
#             api_key=QDRANT_API_KEY,
#         )

#         self.vector_size = 1024  # Gemini embedding size
#         self._detect_search_method()

#     def _detect_search_method(self):
#         """Detect which search method to use based on available methods"""
#         if hasattr(self.client, 'search'):
#             self.search_method = 'search'
#             print("✅ Using 'search' method")
#         elif hasattr(self.client, 'query_points'):
#             self.search_method = 'query_points'
#             print("✅ Using 'query_points' method")
#         elif hasattr(self.client, 'search_points'):
#             self.search_method = 'search_points'
#             print("✅ Using 'search_points' method")
#         else:
#             raise AttributeError("No search method found in QdrantClient!")

#     def ensure_collection_exists(self):
#         try:
#             info = self.client.get_collection(self.collection_name)

#             if info.config.params.vectors.size == self.vector_size:
#                 print(f"✅ Collection '{self.collection_name}' exists.")
#                 return

#             print("⚠️ Vector size mismatch → recreating.")

#         except Exception:
#             print(f"Collection '{self.collection_name}' missing → creating.")

#         self.client.recreate_collection(
#             collection_name=self.collection_name,
#             vectors_config=models.VectorParams(
#                 size=self.vector_size,
#                 distance=models.Distance.COSINE,
#             )
#         )

#     def upsert_vectors(self, vectors, payloads):
#         ids = [str(uuid.uuid4()) for _ in vectors]

#         self.client.upsert(
#             collection_name=self.collection_name,
#             points=models.Batch(
#                 ids=ids,
#                 vectors=vectors,
#                 payloads=payloads,
#             ),
#         )

#         print(f"✅ Upserted {len(vectors)} vectors.")

#     def search(self, query_vector, limit=5):
#         """Universal search method that works with any Qdrant version"""
        
#         if self.search_method == 'search':
#             # For newer versions
#             result = self.client.search(
#                 collection_name=self.collection_name,
#                 query_vector=query_vector,
#                 limit=limit,
#                 with_payload=True,
#             )
            
#         elif self.search_method == 'query_points':
#             # For Qdrant 1.0+
#             result = self.client.query_points(
#                 collection_name=self.collection_name,
#                 query=models.Nearest(
#                     vector=query_vector,
#                 ),
#                 limit=limit,
#                 with_payload=True,
#             )
#             result = result.points
            
#         elif self.search_method == 'search_points':
#             # For older versions
#             result = self.client.search_points(
#                 collection_name=self.collection_name,
#                 vector=query_vector,
#                 limit=limit,
#                 with_payload=True,
#             )
        
#         # Extract payloads
#         payloads = []
#         for hit in result:
#             if hasattr(hit, 'payload'):
#                 payloads.append(hit.payload)
#             elif isinstance(hit, dict) and 'payload' in hit:
#                 payloads.append(hit['payload'])
        
#         return payloads


# # Test it
# qdrant_db = QdrantDB()


import os
import uuid
from typing import List, Dict, Any
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Missing QDRANT_URL or QDRANT_API_KEY")


class QdrantDB:
    def __init__(self, collection_name: str = "docs"):
        self.collection_name = collection_name
        self.vector_size = 1024  # Gemini embedding size

        # Connect to Qdrant
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )

        print("✅ Connected to Qdrant Cloud")

    # ---------------------------------------------------
    # Create or recreate collection
    # ---------------------------------------------------
    def ensure_collection_exists(self):
        try:
            info = self.client.get_collection(self.collection_name)

            if info.config.params.vectors.size == self.vector_size:
                print(f"✅ Collection '{self.collection_name}' exists.")
                return

            print("⚠️ Vector size mismatch — recreating collection...")

        except Exception:
            print(f"📁 Creating new collection '{self.collection_name}'")

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE
            )
        )

    # ---------------------------------------------------
    # Insert vectors + text payload
    # ---------------------------------------------------
    def upsert_vectors(self, vectors: List[List[float]], payloads: List[Dict]):
        ids = [str(uuid.uuid4()) for _ in vectors]

        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=ids,
                vectors=vectors,
                payloads=payloads,
            )
        )

        print(f"✅ Inserted {len(vectors)} vectors")

    # ---------------------------------------------------
    # Universal Search — Works on ALL Qdrant versions
    # ---------------------------------------------------
    def search(self, query_vector: List[float], limit: int = 5):
        try:
            result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
            )

            return [hit.payload for hit in result]

        except Exception as e:
            print(f"❌ Qdrant search failed: {e}")
            return []

    # ---------------------------------------------------
    # Debugging: Collection Info
    # ---------------------------------------------------
    def debug_collection_info(self):
        try:
            info = self.client.get_collection(self.collection_name)
            print(f"\n📊 Collection: {self.collection_name}")
            print(f"   Points: {info.points_count}")
            print(f"   Vector Size: {info.config.params.vectors.size}")
            print(f"   Distance: {info.config.params.vectors.distance}")

            return info.points_count

        except Exception as e:
            print(f"❌ Cannot fetch collection info: {e}")
            return 0

    # ---------------------------------------------------
    # Debugging: Sample Points
    # ---------------------------------------------------
    def debug_sample_points(self, limit: int = 3):
        try:
            print(f"\n🔍 Fetching {limit} sample points...")

            points, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=False,
            )

            if not points:
                print("   No points found.")
                return

            for p in points:
                print(f"\n🟦 Point ID: {p.id}")
                print(f"   Keys: {list(p.payload.keys())}")
                if "text" in p.payload:
                    preview = p.payload["text"][:100]
                    print(f"   Text Preview: {preview}...")

        except Exception as e:
            print(f"❌ Error fetching sample points: {e}")

    # ---------------------------------------------------
    # Test Search with Dummy Vector
    # ---------------------------------------------------
    def test_search_with_dummy_vector(self):
        print("\n🧪 Testing search with dummy zero-vector...")

        dummy = [0.0] * self.vector_size

        try:
            res = self.search(dummy, limit=3)
            print(f"   Results found: {len(res)}")

            for r in res:
                print(r)

        except Exception as e:
            print(f"❌ Dummy search failed: {e}")

    # ---------------------------------------------------
    # Insert Sample Data (Optional)
    # ---------------------------------------------------
    def insert_sample_data(self):
        docs = [
            {"text": "Python is a programming language.", "source": "sample"},
            {"text": "Qdrant is a vector database.", "source": "sample"},
            {"text": "FastAPI is a Python web framework.", "source": "sample"},
        ]

        vectors = []
        for i in range(len(docs)):
            v = [0.01 * (i + 1)] * self.vector_size  # dummy embedding
            vectors.append(v)

        self.upsert_vectors(vectors, docs)
        print("✅ Sample data added!")


# Export instance for import everywhere
qdrant_db = QdrantDB()


# ---------------------------------------------------
# Run debug only when run directly
# ---------------------------------------------------
if __name__ == "__main__":
    qdrant_db.ensure_collection_exists()

    count = qdrant_db.debug_collection_info()
    qdrant_db.debug_sample_points()

    if count == 0:
        print("\n⚠️ Collection empty, inserting sample data...")
        qdrant_db.insert_sample_data()

    qdrant_db.test_search_with_dummy_vector()
