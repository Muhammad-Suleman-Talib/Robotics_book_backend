# backend/agent_config.py

import os
from typing import List, Dict, Any

import google.generativeai as genai
from dotenv import load_dotenv

from backend.prompt import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=GOOGLE_API_KEY)


class RAGAgent:
    """
    The reasoning agent for the RAG chatbot. It uses a Gemini model
    to generate answers based on a system prompt and retrieved context.
    """

    def __init__(self, model_name: str = "gemini-pro"):
        """
        Initializes the agent with a specific Gemini model.

        Args:
            model_name (str): The name of the generative model to use.
        """
        self.model = genai.GenerativeModel(
            model_name,
            system_instruction=SYSTEM_PROMPT
        )
        self.chat = self.model.start_chat(history=[])

    def get_response(self, query: str, context: List[Dict[str, Any]]) -> str:
        """
        Generates a response based on the user's query and the retrieved context.

        Args:
            query (str): The user's question.
            context (List[Dict[str, Any]]): A list of document chunks retrieved
                                             from the vector database.

        Returns:
            str: The agent's generated response.
        """
        if not context:
            return "I am sorry, but the provided text does not contain the answer to this question."

        # Format the context for the prompt
        context_str = "\n---\n".join([doc["chunk"] for doc in context])

        # Construct the final prompt for the model
        prompt = f"""
        CONTEXT:
        {context_str}
        
        QUESTION:
        {query}
        
        ANSWER:
        """

        try:
            # Send the prompt to the Gemini model
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            print(f"An error occurred while generating the response: {e}")
            return "Sorry, I encountered an error while trying to generate a response."


# Singleton instance
rag_agent = RAGAgent()
