from langchain_core.chat_history import InMemoryChatMessageHistory
from typing import Dict

store: Dict[str, InMemoryChatMessageHistory] = {}

class MemoryService:
    @staticmethod
    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    @staticmethod
    def reset_session(session_id: str):
        if session_id in store:
            store[session_id] = InMemoryChatMessageHistory()
