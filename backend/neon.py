# backend/neon.py

import os
import asyncpg
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")
if not NEON_DATABASE_URL:
    raise ValueError("NEON_DATABASE_URL environment variable must be set.")


class NeonDB:
    """
    An asynchronous client for interacting with a Neon Postgres database.
    """

    def __init__(self, dsn: str):
        self.dsn = dsn
        self._pool = None

    async def _get_pool(self):
        """Lazily creates and returns a connection pool."""
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self.dsn)
        return self._pool

    async def init_db(self):
        """
        Initializes the database by creating the chat_history table if it doesn't exist.
        """
        pool = await self._get_pool()
        async with pool.acquire() as connection:
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL, -- 'user' or 'assistant'
                    message TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS ingested_files (
                    id SERIAL PRIMARY KEY,
                    file_name VARCHAR(255) NOT NULL,
                    file_path TEXT NOT NULL,
                    total_chunks INTEGER NOT NULL,
                    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (file_path)
                );
            """)
            print("Database initialized: 'chat_history' and 'ingested_files' tables ensured.")

    async def add_chat_message(self, session_id: str, role: str, message: str):
        """
        Adds a new chat message to the chat_history table.

        Args:
            session_id (str): The unique identifier for the chat session.
            role (str): The role of the message sender ('user' or 'assistant').
            message (str): The content of the message.
        """
        pool = await self._get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO chat_history (session_id, role, message)
                VALUES ($1, $2, $3);
                """,
                session_id,
                role,
                message,
            )

    async def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the chat history for a given session ID.

        Args:
            session_id (str): The unique identifier for the chat session.

        Returns:
            List[Dict[str, Any]]: A list of messages, ordered by creation time.
        """
        pool = await self._get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                """
                SELECT role, message
                FROM chat_history
                WHERE session_id = $1
                ORDER BY created_at ASC;
                """,
                session_id,
            )
        return [dict(row) for row in rows]
    
    async def add_ingested_file_metadata(self, file_name: str, file_path: str, total_chunks: int):
        """
        Adds metadata for an ingested file to the ingested_files table.

        Args:
            file_name (str): The name of the file.
            file_path (str): The full path to the file.
            total_chunks (int): The total number of chunks generated from the file.
        """
        pool = await self._get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO ingested_files (file_name, file_path, total_chunks)
                VALUES ($1, $2, $3)
                ON CONFLICT (file_path) DO UPDATE SET total_chunks = $3;
                """,
                file_name,
                file_path,
                total_chunks,
            )

    async def get_ingested_file_metadata(self) -> List[Dict[str, Any]]:
        """
        Retrieves metadata for all ingested files.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a file's metadata.
        """
        pool = await self._get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                """
                SELECT id, file_name, file_path, total_chunks, ingestion_timestamp
                FROM ingested_files
                ORDER BY ingestion_timestamp DESC;
                """
            )
        return [dict(row) for row in rows]


# Singleton instance
neon_db = NeonDB(dsn=NEON_DATABASE_URL)
