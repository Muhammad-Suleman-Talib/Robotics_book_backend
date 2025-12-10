# # backend/agent_config.py

# import os
# from typing import List, Dict, Any

# from openai import OpenAI
# from dotenv import load_dotenv

# from backend.prompt import SYSTEM_PROMPT

# # Load environment variables
# load_dotenv()

# # OpenAI-compatible API Key and Base URL
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY environment variable not set. This should be your Gemini API key if using a compatible proxy.")
# # OPENAI_API_BASE can be optional if using default OpenAI endpoints,
# # but required if pointing to a custom proxy for Gemini.


# class RAGAgent:
#     """
#     The reasoning agent for the RAG chatbot. It uses an OpenAI-compatible client
#     (configured to use Gemini via proxy/endpoint if OPENAI_API_BASE is set)
#     to generate answers based on a system prompt and retrieved context.
#     """

#     def __init__(self, model: str = "gemini-2.5-flash"): # Use a model name compatible with the proxy/Gemini
#         """
#         Initializes the agent with a specific model.

#         Args:
#             model (str): The name of the generative model to use (e.g., "gemini-pro").
#         """
#         self.model = model
#         self.client = OpenAI(
#             api_key=OPENAI_API_KEY,
#             base_url=OPENAI_API_BASE if OPENAI_API_BASE else None,
#         )

#     def get_response(self, query: str, context: List[Dict[str, Any]]) -> str:
#         """
#         Generates a response based on the user's query and the retrieved context.

#         Args:
#             query (str): The user's question.
#             context (List[Dict[str, Any]]): A list of document chunks retrieved
#                                              from the vector database.

#         Returns:
#             str: The agent's generated response.
#         """
#         if not context:
#             # If no context, the system prompt dictates the response.
#             # We still need to pass it to the LLM to get the exact phrasing.
#             messages = [
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": f"QUESTION: {query}\nANSWER:"}
#             ]
#         else:
#             # Format the context for the prompt
#             context_str = "\n---\n".join([doc["chunk"] for doc in context])

#             messages = [
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": f"CONTEXT:\n{context_str}\n\nQUESTION:\n{query}\n\nANSWER:"}
#             ]

#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 temperature=0.0, # Make response deterministic
#                 max_tokens=500, # Limit response length
#             )
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             print(f"An error occurred while generating the response: {e}")
#             return "Sorry, I encountered an error while trying to generate a response."


# # Singleton instance
# rag_agent = RAGAgent()




# backend/agent_config.py

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GENAI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GENAI_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


class RAGAgent:
    def get_response(self, query, context):

        context_text = "\n\n".join([c["chunk"] for c in context]) if context else ""

        prompt = f"""
        You are a helpful assistant.
        Answer ONLY using the context below.

        Context:
        {context_text}

        Question:
        {query}

        If the answer is not in context → reply exactly:
        "I cannot find the answer in the provided context."
        """

        response = model.generate_content(prompt)

        return response.text


rag_agent = RAGAgent()
