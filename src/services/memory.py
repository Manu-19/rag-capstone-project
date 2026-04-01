# memory.py
from langchain_core.chat_history import InMemoryChatMessageHistory
from typing import Dict

# Dictionary to store session histories
store: Dict[str, InMemoryChatMessageHistory] = {}

class MemoryService:
    @staticmethod
    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        """
        Returns an in-memory chat message history for a given session.
        If the session does not exist, it creates a new one.
        """
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    @staticmethod
    def reset_session(session_id: str):
        """
        Clears the chat history for a given session.
        """
        if session_id in store:
            store[session_id] = InMemoryChatMessageHistory()